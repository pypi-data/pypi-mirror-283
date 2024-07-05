# Copyright 2021 The HuggingFace Team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
import inspect
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import contextmanager
from functools import partial
from pathlib import Path
from typing import List, Union
from unittest import mock

import torch

import accelerate

from ..state import AcceleratorState, PartialState
from ..utils import (
    gather,
    is_bnb_available,
    is_clearml_available,
    is_comet_ml_available,
    is_cuda_available,
    is_datasets_available,
    is_deepspeed_available,
    is_dvclive_available,
    is_import_timer_available,
    is_mlu_available,
    is_mps_available,
    is_npu_available,
    is_pandas_available,
    is_pippy_available,
    is_schedulefree_available,
    is_tensorboard_available,
    is_timm_available,
    is_torch_version,
    is_torch_xla_available,
    is_torchvision_available,
    is_transformers_available,
    is_triton_available,
    is_wandb_available,
    is_xpu_available,
    str_to_bool,
)


def get_backend():
    if is_torch_xla_available():
        return "xla", torch.cuda.device_count(), torch.cuda.memory_allocated
    elif is_cuda_available():
        return "cuda", torch.cuda.device_count(), torch.cuda.memory_allocated
    elif is_mps_available(min_version="2.0"):
        return "mps", 1, torch.mps.current_allocated_memory
    elif is_mps_available():
        return "mps", 1, lambda: 0
    elif is_mlu_available():
        return "mlu", torch.mlu.device_count(), torch.mlu.memory_allocated
    elif is_npu_available():
        return "npu", torch.npu.device_count(), torch.npu.memory_allocated
    elif is_xpu_available():
        return "xpu", torch.xpu.device_count(), torch.xpu.memory_allocated
    else:
        return "cpu", 1, lambda: 0


torch_device, device_count, memory_allocated_func = get_backend()


def get_launch_command(**kwargs) -> list:
    """
    Wraps around `kwargs` to help simplify launching from `subprocess`.

    Example:
    ```python
    # returns ['accelerate', 'launch', '--num_processes=2', '--device_count=2']
    get_launch_command(num_processes=2, device_count=2)
    ```
    """
    command = ["accelerate", "launch"]
    for k, v in kwargs.items():
        if isinstance(v, bool) and v:
            command.append(f"--{k}")
        elif v is not None:
            command.append(f"--{k}={v}")
    return command


DEFAULT_LAUNCH_COMMAND = get_launch_command(num_processes=device_count, monitor_interval=0.1)


def parse_flag_from_env(key, default=False):
    try:
        value = os.environ[key]
    except KeyError:
        # KEY isn't set, default to `default`.
        _value = default
    else:
        # KEY is set, convert it to True or False.
        try:
            _value = str_to_bool(value)
        except ValueError:
            # More values are supported, but let's keep the message simple.
            raise ValueError(f"If set, {key} must be yes or no.")
    return _value


_run_slow_tests = parse_flag_from_env("RUN_SLOW", default=False)


def skip(test_case):
    "Decorator that skips a test unconditionally"
    return unittest.skip("Test was skipped")(test_case)


def slow(test_case):
    """
    Decorator marking a test as slow. Slow tests are skipped by default. Set the RUN_SLOW environment variable to a
    truthy value to run them.
    """
    return unittest.skipUnless(_run_slow_tests, "test is slow")(test_case)


def require_cpu(test_case):
    """
    Decorator marking a test that must be only ran on the CPU. These tests are skipped when a GPU is available.
    """
    return unittest.skipUnless(torch_device == "cpu", "test requires only a CPU")(test_case)


def require_non_cpu(test_case):
    """
    Decorator marking a test that requires a hardware accelerator backend. These tests are skipped when there are no
    hardware accelerator available.
    """
    return unittest.skipUnless(torch_device != "cpu", "test requires a GPU")(test_case)


def require_cuda(test_case):
    """
    Decorator marking a test that requires CUDA. These tests are skipped when there are no GPU available or when
    TorchXLA is available.
    """
    return unittest.skipUnless(is_cuda_available() and not is_torch_xla_available(), "test requires a GPU")(test_case)


def require_xpu(test_case):
    """
    Decorator marking a test that requires XPU. These tests are skipped when there are no XPU available.
    """
    return unittest.skipUnless(is_xpu_available(), "test requires a XPU")(test_case)


def require_non_xpu(test_case):
    """
    Decorator marking a test that should be skipped for XPU.
    """
    return unittest.skipUnless(torch_device != "xpu", "test requires a non-XPU")(test_case)


def require_mlu(test_case):
    """
    Decorator marking a test that requires MLU. These tests are skipped when there are no MLU available.
    """
    return unittest.skipUnless(is_mlu_available(), "test require a MLU")(test_case)


def require_npu(test_case):
    """
    Decorator marking a test that requires NPU. These tests are skipped when there are no NPU available.
    """
    return unittest.skipUnless(is_npu_available(), "test require a NPU")(test_case)


def require_mps(test_case):
    """
    Decorator marking a test that requires MPS backend. These tests are skipped when torch doesn't support `mps`
    backend.
    """
    return unittest.skipUnless(is_mps_available(), "test requires a `mps` backend support in `torch`")(test_case)


def require_huggingface_suite(test_case):
    """
    Decorator marking a test that requires transformers and datasets. These tests are skipped when they are not.
    """
    return unittest.skipUnless(
        is_transformers_available() and is_datasets_available(),
        "test requires the Hugging Face suite",
    )(test_case)


def require_transformers(test_case):
    """
    Decorator marking a test that requires transformers. These tests are skipped when they are not.
    """
    return unittest.skipUnless(is_transformers_available(), "test requires the transformers library")(test_case)


def require_timm(test_case):
    """
    Decorator marking a test that requires timm. These tests are skipped when they are not.
    """
    return unittest.skipUnless(is_timm_available(), "test requires the timm library")(test_case)


def require_torchvision(test_case):
    """
    Decorator marking a test that requires torchvision. These tests are skipped when they are not.
    """
    return unittest.skipUnless(is_torchvision_available(), "test requires the torchvision library")(test_case)


def require_triton(test_case):
    """
    Decorator marking a test that requires triton. These tests are skipped when they are not.
    """
    return unittest.skipUnless(is_triton_available(), "test requires the triton library")(test_case)


def require_schedulefree(test_case):
    """
    Decorator marking a test that requires schedulefree. These tests are skipped when they are not.
    """
    return unittest.skipUnless(is_schedulefree_available(), "test requires the schedulefree library")(test_case)


def require_bnb(test_case):
    """
    Decorator marking a test that requires bitsandbytes. These tests are skipped when they are not.
    """
    return unittest.skipUnless(is_bnb_available(), "test requires the bitsandbytes library")(test_case)


def require_tpu(test_case):
    """
    Decorator marking a test that requires TPUs. These tests are skipped when there are no TPUs available.
    """
    return unittest.skipUnless(is_torch_xla_available(check_is_tpu=True), "test requires TPU")(test_case)


def require_non_torch_xla(test_case):
    """
    Decorator marking a test as requiring an environment without TorchXLA. These tests are skipped when TorchXLA is
    available.
    """
    return unittest.skipUnless(not is_torch_xla_available(), "test requires an env without TorchXLA")(test_case)


def require_single_device(test_case):
    """
    Decorator marking a test that requires a single device. These tests are skipped when there is no hardware
    accelerator available or number of devices is more than one.
    """
    return unittest.skipUnless(torch_device != "cpu" and device_count == 1, "test requires a hardware accelerator")(
        test_case
    )


def require_single_gpu(test_case):
    """
    Decorator marking a test that requires CUDA on a single GPU. These tests are skipped when there are no GPU
    available or number of GPUs is more than one.
    """
    return unittest.skipUnless(torch.cuda.device_count() == 1, "test requires a GPU")(test_case)


def require_single_xpu(test_case):
    """
    Decorator marking a test that requires CUDA on a single XPU. These tests are skipped when there are no XPU
    available or number of xPUs is more than one.
    """
    return unittest.skipUnless(torch.xpu.device_count() == 1, "test requires a XPU")(test_case)


def require_multi_device(test_case):
    """
    Decorator marking a test that requires a multi-device setup. These tests are skipped on a machine without multiple
    devices.
    """
    return unittest.skipUnless(device_count > 1, "test requires multiple hardware accelerators")(test_case)


def require_multi_gpu(test_case):
    """
    Decorator marking a test that requires a multi-GPU setup. These tests are skipped on a machine without multiple
    GPUs.
    """
    return unittest.skipUnless(torch.cuda.device_count() > 1, "test requires multiple GPUs")(test_case)


def require_multi_xpu(test_case):
    """
    Decorator marking a test that requires a multi-XPU setup. These tests are skipped on a machine without multiple
    XPUs.
    """
    return unittest.skipUnless(torch.xpu.device_count() > 1, "test requires multiple XPUs")(test_case)


def require_deepspeed(test_case):
    """
    Decorator marking a test that requires DeepSpeed installed. These tests are skipped when DeepSpeed isn't installed
    """
    return unittest.skipUnless(is_deepspeed_available(), "test requires DeepSpeed")(test_case)


def require_fsdp(test_case):
    """
    Decorator marking a test that requires FSDP installed. These tests are skipped when FSDP isn't installed
    """
    return unittest.skipUnless(is_torch_version(">=", "1.12.0"), "test requires torch version >= 1.12.0")(test_case)


def require_torch_min_version(test_case=None, version=None):
    """
    Decorator marking that a test requires a particular torch version to be tested. These tests are skipped when an
    installed torch version is less than the required one.
    """
    if test_case is None:
        return partial(require_torch_min_version, version=version)
    return unittest.skipUnless(is_torch_version(">=", version), f"test requires torch version >= {version}")(test_case)


def require_tensorboard(test_case):
    """
    Decorator marking a test that requires tensorboard installed. These tests are skipped when tensorboard isn't
    installed
    """
    return unittest.skipUnless(is_tensorboard_available(), "test requires Tensorboard")(test_case)


def require_wandb(test_case):
    """
    Decorator marking a test that requires wandb installed. These tests are skipped when wandb isn't installed
    """
    return unittest.skipUnless(is_wandb_available(), "test requires wandb")(test_case)


def require_comet_ml(test_case):
    """
    Decorator marking a test that requires comet_ml installed. These tests are skipped when comet_ml isn't installed
    """
    return unittest.skipUnless(is_comet_ml_available(), "test requires comet_ml")(test_case)


def require_clearml(test_case):
    """
    Decorator marking a test that requires clearml installed. These tests are skipped when clearml isn't installed
    """
    return unittest.skipUnless(is_clearml_available(), "test requires clearml")(test_case)


def require_dvclive(test_case):
    """
    Decorator marking a test that requires dvclive installed. These tests are skipped when dvclive isn't installed
    """
    return unittest.skipUnless(is_dvclive_available(), "test requires dvclive")(test_case)


def require_pandas(test_case):
    """
    Decorator marking a test that requires pandas installed. These tests are skipped when pandas isn't installed
    """
    return unittest.skipUnless(is_pandas_available(), "test requires pandas")(test_case)


def require_pippy(test_case):
    """
    Decorator marking a test that requires pippy installed. These tests are skipped when pippy isn't installed
    """
    return unittest.skipUnless(is_pippy_available(), "test requires pippy")(test_case)


def require_import_timer(test_case):
    """
    Decorator marking a test that requires tuna interpreter installed. These tests are skipped when tuna isn't
    installed
    """
    return unittest.skipUnless(is_import_timer_available(), "test requires tuna interpreter")(test_case)


_atleast_one_tracker_available = (
    any([is_wandb_available(), is_tensorboard_available()]) and not is_comet_ml_available()
)


def require_trackers(test_case):
    """
    Decorator marking that a test requires at least one tracking library installed. These tests are skipped when none
    are installed
    """
    return unittest.skipUnless(
        _atleast_one_tracker_available,
        "test requires at least one tracker to be available and for `comet_ml` to not be installed",
    )(test_case)


class TempDirTestCase(unittest.TestCase):
    """
    A TestCase class that keeps a single `tempfile.TemporaryDirectory` open for the duration of the class, wipes its
    data at the start of a test, and then destroyes it at the end of the TestCase.

    Useful for when a class or API requires a single constant folder throughout it's use, such as Weights and Biases

    The temporary directory location will be stored in `self.tmpdir`
    """

    clear_on_setup = True

    @classmethod
    def setUpClass(cls):
        "Creates a `tempfile.TemporaryDirectory` and stores it in `cls.tmpdir`"
        cls.tmpdir = Path(tempfile.mkdtemp())

    @classmethod
    def tearDownClass(cls):
        "Remove `cls.tmpdir` after test suite has finished"
        if os.path.exists(cls.tmpdir):
            shutil.rmtree(cls.tmpdir)

    def setUp(self):
        "Destroy all contents in `self.tmpdir`, but not `self.tmpdir`"
        if self.clear_on_setup:
            for path in self.tmpdir.glob("**/*"):
                if path.is_file():
                    path.unlink()
                elif path.is_dir():
                    shutil.rmtree(path)


class AccelerateTestCase(unittest.TestCase):
    """
    A TestCase class that will reset the accelerator state at the end of every test. Every test that checks or utilizes
    the `AcceleratorState` class should inherit from this to avoid silent failures due to state being shared between
    tests.
    """

    def tearDown(self):
        super().tearDown()
        # Reset the state of the AcceleratorState singleton.
        AcceleratorState._reset_state()
        PartialState._reset_state()


class MockingTestCase(unittest.TestCase):
    """
    A TestCase class designed to dynamically add various mockers that should be used in every test, mimicking the
    behavior of a class-wide mock when defining one normally will not do.

    Useful when a mock requires specific information available only initialized after `TestCase.setUpClass`, such as
    setting an environment variable with that information.

    The `add_mocks` function should be ran at the end of a `TestCase`'s `setUp` function, after a call to
    `super().setUp()` such as:
    ```python
    def setUp(self):
        super().setUp()
        mocks = mock.patch.dict(os.environ, {"SOME_ENV_VAR", "SOME_VALUE"})
        self.add_mocks(mocks)
    ```
    """

    def add_mocks(self, mocks: Union[mock.Mock, List[mock.Mock]]):
        """
        Add custom mocks for tests that should be repeated on each test. Should be called during
        `MockingTestCase.setUp`, after `super().setUp()`.

        Args:
            mocks (`mock.Mock` or list of `mock.Mock`):
                Mocks that should be added to the `TestCase` after `TestCase.setUpClass` has been run
        """
        self.mocks = mocks if isinstance(mocks, (tuple, list)) else [mocks]
        for m in self.mocks:
            m.start()
            self.addCleanup(m.stop)


def are_the_same_tensors(tensor):
    state = AcceleratorState()
    tensor = tensor[None].clone().to(state.device)
    tensors = gather(tensor).cpu()
    tensor = tensor[0].cpu()
    for i in range(tensors.shape[0]):
        if not torch.equal(tensors[i], tensor):
            return False
    return True


class _RunOutput:
    def __init__(self, returncode, stdout, stderr):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


async def _read_stream(stream, callback):
    while True:
        line = await stream.readline()
        if line:
            callback(line)
        else:
            break


async def _stream_subprocess(cmd, env=None, stdin=None, timeout=None, quiet=False, echo=False) -> _RunOutput:
    if echo:
        print("\nRunning: ", " ".join(cmd))

    p = await asyncio.create_subprocess_exec(
        cmd[0],
        *cmd[1:],
        stdin=stdin,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env=env,
    )

    # note: there is a warning for a possible deadlock when using `wait` with huge amounts of data in the pipe
    # https://docs.python.org/3/library/asyncio-subprocess.html#asyncio.asyncio.subprocess.Process.wait
    #
    # If it starts hanging, will need to switch to the following code. The problem is that no data
    # will be seen until it's done and if it hangs for example there will be no debug info.
    # out, err = await p.communicate()
    # return _RunOutput(p.returncode, out, err)

    out = []
    err = []

    def tee(line, sink, pipe, label=""):
        line = line.decode("utf-8").rstrip()
        sink.append(line)
        if not quiet:
            print(label, line, file=pipe)

    # XXX: the timeout doesn't seem to make any difference here
    await asyncio.wait(
        [
            asyncio.create_task(_read_stream(p.stdout, lambda l: tee(l, out, sys.stdout, label="stdout:"))),
            asyncio.create_task(_read_stream(p.stderr, lambda l: tee(l, err, sys.stderr, label="stderr:"))),
        ],
        timeout=timeout,
    )
    return _RunOutput(await p.wait(), out, err)


def execute_subprocess_async(cmd: list, env=None, stdin=None, timeout=180, quiet=False, echo=True) -> _RunOutput:
    # Cast every path in `cmd` to a string
    for i, c in enumerate(cmd):
        if isinstance(c, Path):
            cmd[i] = str(c)
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(
        _stream_subprocess(cmd, env=env, stdin=stdin, timeout=timeout, quiet=quiet, echo=echo)
    )

    cmd_str = " ".join(cmd)
    if result.returncode > 0:
        stderr = "\n".join(result.stderr)
        raise RuntimeError(
            f"'{cmd_str}' failed with returncode {result.returncode}\n\n"
            f"The combined stderr from workers follows:\n{stderr}"
        )

    return result


class SubprocessCallException(Exception):
    pass


def run_command(command: List[str], return_stdout=False, env=None):
    """
    Runs `command` with `subprocess.check_output` and will potentially return the `stdout`. Will also properly capture
    if an error occured while running `command`
    """
    # Cast every path in `command` to a string
    for i, c in enumerate(command):
        if isinstance(c, Path):
            command[i] = str(c)
    if env is None:
        env = os.environ.copy()
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, env=env)
        if return_stdout:
            if hasattr(output, "decode"):
                output = output.decode("utf-8")
            return output
    except subprocess.CalledProcessError as e:
        raise SubprocessCallException(
            f"Command `{' '.join(command)}` failed with the following error:\n\n{e.output.decode()}"
        ) from e


def path_in_accelerate_package(*components: str) -> Path:
    """
    Get a path within the `accelerate` package's directory.

    Args:
        *components: Components of the path to join after the package directory.

    Returns:
        `Path`: The path to the requested file or directory.
    """

    accelerate_package_dir = Path(inspect.getfile(accelerate)).parent
    return accelerate_package_dir.joinpath(*components)


@contextmanager
def assert_exception(exception_class: Exception, msg: str = None) -> bool:
    """
    Context manager to assert that the right `Exception` class was raised.

    If `msg` is provided, will check that the message is contained in the raised exception.
    """
    was_ran = False
    try:
        yield
        was_ran = True
    except Exception as e:
        assert isinstance(e, exception_class), f"Expected exception of type {exception_class} but got {type(e)}"
        if msg is not None:
            assert msg in str(e), f"Expected message '{msg}' to be in exception but got '{str(e)}'"
    if was_ran:
        raise AssertionError(f"Expected exception of type {exception_class} but ran without issue.")
