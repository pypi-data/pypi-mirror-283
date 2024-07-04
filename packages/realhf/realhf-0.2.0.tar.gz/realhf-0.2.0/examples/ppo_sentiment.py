import argparse
import dataclasses
from typing import Dict, List, Optional

import colorama
import torch
import transformers

from realhf.api.core import config as config_api
from realhf.api.core import dfg, model_api, system_api
from realhf.api.core.system_api import ExperimentConfig
from realhf.api.quickstart.entrypoint import register_quickstart_exp
from realhf.apps.quickstart import main
from realhf.base import logging
from realhf.base.namedarray import NamedArray
from realhf.experiments.common.ppo_exp import PPOConfig

logger = logging.getLogger("Sentiment PPO example")


@dataclasses.dataclass
class SentimentScoringInterface(model_api.ModelInterface):

    def __post_init__(self):
        super().__post_init__()
        self.score_model = (
            transformers.AutoModelForSequenceClassification.from_pretrained(
                "/path/to/score_model"
            ).cuda()
        )
        self.score_model.eval()

        self.score_tokenizer = transformers.AutoTokenizer.from_pretrained(
            "/path/to/score_model"
        )

    @torch.no_grad()
    def inference(self, model: model_api.Model, data: NamedArray) -> NamedArray:
        packed_input_ids: torch.Tensor = data["packed_input_ids"]
        seqlens_cpu: List[int] = data.metadata["seqlens"]
        max_seqlen = max(seqlens_cpu)
        bs = len(seqlens_cpu)
        device = packed_input_ids.device

        # Build attention mask.
        _ind = torch.arange(max_seqlen, dtype=torch.long, device=device)
        _seqlens = torch.tensor(seqlens_cpu, dtype=torch.long, device=device)
        attention_mask = _ind.unsqueeze(0) < _seqlens.unsqueeze(1)

        # Pad input_ids.
        input_ids = torch.full(
            (bs * max_seqlen,),
            fill_value=model.tokenizer.pad_token_id,
            device=device,
            dtype=torch.long,
        )
        indices = torch.nonzero(attention_mask.flatten(), as_tuple=False).flatten()
        input_ids[indices] = packed_input_ids
        input_ids = input_ids.view(bs, max_seqlen)

        # Re-tokenize.
        texts = model.tokenizer.batch_decode(input_ids, skip_special_tokens=True)
        encoding = self.score_tokenizer(
            texts, return_tensors="pt", padding=True, truncation=True
        )

        # Inference to get the score.
        logits = self.score_model(
            input_ids=encoding["input_ids"].cuda(),
            attention_mask=encoding["attention_mask"].cuda(),
        ).logits
        # For IMDB, 0 is negative and 1 is positive. We record the logits of positive.
        scores = logits[..., -1].contiguous().float()
        assert scores.shape == (bs,), scores.shape

        # ###################### logging ######################
        # for text, score in zip(texts, scores):
        #     logger.info(
        #         f"reward is {colorama.Fore.RED}{score.item()}{colorama.Style.RESET_ALL}, "
        #         f"sequence is: {colorama.Fore.YELLOW + colorama.Style.DIM}{text}{colorama.Style.RESET_ALL}"
        #     )
        # #####################################################

        res = NamedArray(scores=scores)
        res.register_metadata(**data.metadata)
        return res


model_api.register_interface("sentiment_scoring", SentimentScoringInterface)


class MyPPOConfig(PPOConfig):

    def initial_setup(self) -> ExperimentConfig:
        if (
            self.rew_inf.parallel.model_parallel_size > 1
            or self.rew_inf.parallel.pipeline_parallel_size > 1
        ):
            raise ValueError(
                "For this example, the reward model does not support model parallel or pipeline parallel."
            )

        cfg = super().initial_setup()

        # Replace the backend and model configurations for the reward model.
        for mw in cfg.model_worker:
            for s in mw.shards:
                if s.id.model_name.role == "reward":
                    s.model = config_api.Model(
                        "tokenizer",
                        args=dict(
                            tokenizer_path=self.rew.path,
                        ),
                    )
                    s.backend = config_api.ModelBackend("null")

        # Change the model function call implementation.
        idx = 0
        for rpc in cfg.model_rpcs:
            if rpc.model_name.role == "reward":
                break
            idx += 1
        inf_reward_rpc = cfg.model_rpcs[idx]
        inf_reward_rpc.interface_impl = dfg.ModelInterface("sentiment_scoring")
        inf_reward_rpc.post_hooks = []

        return cfg


register_quickstart_exp("my-ppo", MyPPOConfig)

if __name__ == "__main__":
    main()
