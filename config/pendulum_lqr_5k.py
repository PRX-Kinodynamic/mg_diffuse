from mg_diffuse.utils import watch, handle_angle_wraparound, augment_unwrapped_state_data

DATASET_SIZE = 5565

# ------------------------ base ------------------------#

## automatically make experiment names for planning
## by labelling folders with these args

args_to_watch = [
    ("prefix", ""),
    ("horizon", "H"),
    ("n_diffusion_steps", "T"),
    ("use_padding", "PAD"),
    ("predict_epsilon", "EPS"),
    ("attention", "ATN"),
    ("loss_discount", "LD"),
    ## value kwargs
    ("discount", "d"),
]

logbase = "experiments"

base = {
    "roa_estimation": {
        "attractors": {
            (-2.1, 0): 0,
            (2.1, 0): 0,
            (0, 0): 1,
        },
        "invalid_label": -1,
        "attractor_threshold": 0.05,
        "n_runs": 20,
        "batch_size": 270000,
        "attractor_probability_upper_threshold": 0.5,
    },

    "diffusion": {
        ## model
        "model": "models.TemporalUnet",
        "diffusion": "models.GaussianDiffusion",
        "horizon": 32,
        "n_diffusion_steps": 20,
        "action_weight": 10,
        "loss_weights": None,
        "loss_discount": 1,
        "predict_epsilon": False,
        "dim_mults": (1, 2, 4, 8),
        "attention": False,
        "clip_denoised": False,
        "observation_dim": 2,
        ## dataset
        "loader": "datasets.TrajectoryDataset",
        "normalizer": "LimitsNormalizer",
        "preprocess_fns": [handle_angle_wraparound, augment_unwrapped_state_data],
        "preprocess_kwargs": {
            "angle_indices": [0],
        },
        "use_padding": True,
        "max_path_length": 502,
        ## serialization
        "logbase": logbase,
        "prefix": "diffusion/",
        "exp_name": watch(args_to_watch),
        ## training
        "n_steps_per_epoch": 10000,
        "loss_type": "l2",
        "n_train_steps": 1e6,
        "batch_size": 32,
        "learning_rate": 2e-4,
        "gradient_accumulate_every": 2,
        "ema_decay": 0.995,
        "save_freq": 200000,
        "sample_freq": 20000,
        "save_parallel": False,
        "n_reference": 8,
        "bucket": None,
        "device": "cuda",
        "seed": None,
        ## visualization
        "sampling_limits": (-1, 1),
        "granularity": 0.01,
    }
}

# ------------------------ overrides ------------------------#

fewer_steps = {
    "diffusion": {
        "n_diffusion_steps": 5,
        "exp_name": watch(args_to_watch),
    }
}

one_step = {
    "diffusion": {
        "n_diffusion_steps": 1,
        "exp_name": watch(args_to_watch),
    }
}

long_horizon = {
    "diffusion": {
        "horizon": 80,
    }
}

longer_horizon = {
    "diffusion": {
        "horizon": 160,
    }
}
