"""
XPU GPU Preflight — ComfyUI server extension
=============================================
Drop into: ComfyUI/custom_nodes/xpu_gpu_preflight.py

No node needed in the workflow. Automatically flushes XPU GPU state
before every generation by monkey-patching PromptExecutor.execute.

Fixes: black images on Intel Arc caused by corrupted VAE GPU state
between runs (missing TDR watchdog / graceful error recovery on XPU).
"""

import gc
import logging

import torch

log = logging.getLogger("XPU-Preflight")


# ── GPU flush ─────────────────────────────────────────────────────────────────

def _flush_xpu_state() -> None:
    """
    Synchronize and empty the XPU (or CUDA) cache before each generation.
    This replicates the GPU state reset that happens when you manually
    re-select the VAE in the ComfyUI UI.
    """
    gc.collect()

    if hasattr(torch, "xpu") and torch.xpu.is_available():
        try:
            torch.xpu.synchronize()
            torch.xpu.empty_cache()
            log.debug("XPU state flushed.")
        except Exception as exc:
            log.warning(f"XPU flush failed (non-fatal): {exc}")

    elif hasattr(torch, "cuda") and torch.cuda.is_available():
        # Harmless on CUDA; lets the file work on mixed setups
        torch.cuda.synchronize()
        torch.cuda.empty_cache()


# ── Monkey-patch ──────────────────────────────────────────────────────────────

def _patch_executor() -> None:
    try:
        import execution

        original_execute = execution.PromptExecutor.execute

        def patched_execute(self, prompt, prompt_id, extra_data=None, execute_outputs=None):
            _flush_xpu_state()
            return original_execute(self, prompt, prompt_id, extra_data, execute_outputs)

        execution.PromptExecutor.execute = patched_execute
        log.info("XPU Preflight active — GPU state will be flushed before every generation.")

    except Exception as exc:
        log.error(f"XPU Preflight could not patch PromptExecutor: {exc}")


_patch_executor()


# ── No nodes registered — this file is a pure server-side extension ───────────

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}
