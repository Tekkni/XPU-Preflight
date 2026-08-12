⚠️ Not a coder — use at your own risk. Tested on Arc B580, ComfyUI 0.32.0, PyTorch 2.13.0+xpu.

I have an Intel Arc B580 and it bothered me that I couldn't use Stable Diffusion models without persistent black images. I found a possible fix by manually re-selecting the VAE between generations — this extension automates that.

It probably won't prevent black images entirely, but it does help stop them from becoming persistent. Without it, once you get a black image, every generation after that goes black too. This extension resets the VAE GPU state before each generation, which breaks that chain.

You're trading a bit of speed for stability. A varied set of Illustrious/NoobAI models were tested.

My working settings:

* Normal VRAM / Reserved 0.5
* PyTorch Cross Attention
* Preview method: Automatic
* RAM Pressure Cache
* --force-non-blocking (not black image related, helps with VRAM transfer)

If black images still persist:

* Add --force-fp16
* Keep steps around ~24

Environment variables:

* UR_L0_USE_RELAXED_ALLOCATION_LIMITS=1
* SYCL_CACHE_PERSISTENT=1


HOW TO INSTALL:

Just drop the file in \custom_nodes\
That's it. IF you WANT a directory just put it in a directory name of your choosing and rename it to __init__.py

To check if it's active your log/console should state: 

XPU Preflight active — GPU state will be flushed before every generation.
