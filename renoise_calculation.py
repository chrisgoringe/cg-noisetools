class SplitSigmasWithRewind:
    @classmethod
    def INPUT_TYPES(s):
        return {"required":
                    {"sigmas": ("SIGMAS", ),
                    "endstep": ("INT", {"default": 0, "min": 0, "max": 10000}),
                    "startstep": ("INT", {"default": 0, "min": 0, "max": 10000}),
                     }
                }
    RETURN_TYPES = ("SIGMAS","SIGMAS","FLOAT")
    RETURN_NAMES = ("high_sigmas", "low_sigmas", "renoise")
    CATEGORY = "noise"

    FUNCTION = "func"

    def func(self, sigmas, endstep, startstep):
        sigmas1 = sigmas[:endstep + 1]
        sigmas2 = sigmas[startstep:]
        delta = (sigmas2[0] - sigmas1[-1])/sigmas[0]
        return (sigmas1, sigmas2, delta)