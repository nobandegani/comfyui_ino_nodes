import hashlib

class InoGetSamplerModel:
    """

    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "config": ("STRING", {
                    "multiline": False,
                    "default": ""
                }),
                "name": ("STRING", {
                    "multiline": False,
                    "default": ""
                }),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "MODEL", "CLIP", "VAE",)
    RETURN_NAMES = ("Config", "Name", "Model", "CLIP", "VAE")
    FUNCTION = "function"

    CATEGORY = "InoNodes"

    def function(self, enabled, config, name):
        if not enabled:
            return config, name, None, None, None

        from nodes import UNETLoader, CLIPLoader, DualCLIPLoader, VAELoader

        unet_loader = UNETLoader()
        load_unet = unet_loader.load_unet(
            unet_name="flux1dev/chroma-unlocked-v33.safetensors",
            weight_dtype="default"
        )

        dual_clip = False
        if dual_clip:
            clip_loader = DualCLIPLoader()
            load_clip = clip_loader.load_clip(
                clip_name1="flux1d/t5/t5xxl_fp16.safetensors",
                clip_name2="flux1d/t5/t5xxl_fp16.safetensors",
                type="chroma",
                device="default",
            )
        else:
            clip_loader = CLIPLoader()
            load_clip = clip_loader.load_clip(
                clip_name="flux1d/t5/t5xxl_fp16.safetensors",
                type="chroma",
                device="default",
            )

        vae_loader = VAELoader()
        load_vae = vae_loader.load_vae(
            vae_name="FLUX1/ae.safetensors",
        )

        return (config, name, load_unet[0], load_clip[0], load_vae[0], )


class InoGetSamplerConfig:
    """

    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 0xffffffffffffffff,
                    "step": 1,
                    "label": "Seed (0 = random)"
                }),
                "config": ("STRING", {
                    "multiline": False,
                    "default": ""
                }),
                "name": ("STRING", {
                    "multiline": False,
                    "default": ""
                }),
                "model": ("MODEL", {}),
                "clip": ("CLIP", {}),
                "positive": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "label": "positive or flux clip l"
                }),
                "negative": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "label": "Negative or flux t5xxl"
                }),
            },
            "optional": {
                "steps": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 100,
                    "step": 1,
                    "label": "(0 = default)"
                }),
                "cfg": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 50,
                    "step": 1,
                    "label": "(0 = default)"
                }),
                "denoise": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 50,
                    "step": 1,
                    "label": "(0 = default)"
                }),
                "sampler_name": ("STRING", {
                    "multiline": False,
                    "default": "default"
                }),
                "scheduler_name": ("STRING", {
                    "multiline": False,
                    "default": "default"
                }),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "INT", "NOISE", "GUIDER", "SAMPLER", "SIGMAS")
    RETURN_NAMES = ("Config", "Name", "seed", "NOISE", "GUIDER", "SAMPLER", "SIGMAS")
    FUNCTION = "function"

    CATEGORY = "InoNodes"

    @classmethod
    def IS_CHANGED(cls, seed, **kwargs):
        m = hashlib.sha256()
        m.update(seed)
        return m.digest().hex()

    def function(self, enabled, seed,
                 config, name,
                 model, clip, positive, negative,
                 steps, cfg, denoise, sampler_name, scheduler_name):
        if not enabled:
            return config, name, seed,

        from nodes import CLIPTextEncode
        from comfy_extras.nodes_flux import CLIPTextEncodeFlux, FluxGuidance

        use_flux_base = True
        use_flux_clip_encoder = True
        if use_flux_clip_encoder:
            clip_encoder = CLIPTextEncodeFlux()
            condition = clip_encoder.encode(
                clip=clip,
                clip_l = positive,
                t5xxl=negative,
                guidance=cfg
            )
        else:
            clip_encoder = CLIPTextEncode()
            condition = clip_encoder.encode(
                clip=clip,
                text=positive,
            )



        return (config, name, seed, )
