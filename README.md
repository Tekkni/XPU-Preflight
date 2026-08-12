⚠️ Not a coder — use at your own risk. Tested on Arc B580, ComfyUI 0.32.0, PyTorch 2.13.0+xpu.

I have an Intel Arc B580 and it bothered me that I couldn't use Stable Diffusion models without persistent black images. I found a possible fix by manually re-selecting the VAE between generations — this extension automates that.

It probably won't prevent black images entirely, but it does help stop them from becoming persistent. Without it, once you get a black image, every generation after that goes black too. This extension resets the VAE GPU state before each generation, which breaks that chain.

You're trading a bit of speed for stability.

