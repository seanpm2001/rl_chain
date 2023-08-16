import sys

sys.path.append("..")

import rl_chain.pick_best_chain as pick_best_chain
from test_utils import MockEncoder

import pytest

encoded_text = "[ e n c o d e d ] "


def test_pickbest_textembedder_missing_context_throws():
    text_embedder = pick_best_chain.PickBestTextEmbedder(model=MockEncoder())
    named_action = {"action": ["0", "1", "2"]}
    event = pick_best_chain.PickBest.Event(
        inputs={}, to_select_from=named_action, based_on={}
    )
    with pytest.raises(ValueError):
        text_embedder.to_vw_format(event)


def test_pickbest_textembedder_missing_actions_throws():
    text_embedder = pick_best_chain.PickBestTextEmbedder(model=MockEncoder())
    event = pick_best_chain.PickBest.Event(
        inputs={}, to_select_from={}, based_on={"context": "context"}
    )
    with pytest.raises(ValueError):
        text_embedder.to_vw_format(event)


def test_pickbest_textembedder_no_label_no_emb():
    text_embedder = pick_best_chain.PickBestTextEmbedder(model=MockEncoder())
    named_actions = {"action1": ["0", "1", "2"]}
    expected = """shared |context context \n|action1 0 \n|action1 1 \n|action1 2 """
    event = pick_best_chain.PickBest.Event(
        inputs={}, to_select_from=named_actions, based_on={"context": "context"}
    )
    vw_ex_str = text_embedder.to_vw_format(event)
    assert vw_ex_str == expected


def test_pickbest_textembedder_w_label_no_score_no_emb():
    text_embedder = pick_best_chain.PickBestTextEmbedder(model=MockEncoder())
    named_actions = {"action1": ["0", "1", "2"]}
    expected = """shared |context context \n|action1 0 \n|action1 1 \n|action1 2 """
    selected = pick_best_chain.PickBest.Selected(index=0, probability=1.0)
    event = pick_best_chain.PickBest.Event(
        inputs={},
        to_select_from=named_actions,
        based_on={"context": "context"},
        selected=selected,
    )
    vw_ex_str = text_embedder.to_vw_format(event)
    assert vw_ex_str == expected


def test_pickbest_textembedder_w_full_label_no_emb():
    text_embedder = pick_best_chain.PickBestTextEmbedder(model=MockEncoder())
    named_actions = {"action1": ["0", "1", "2"]}
    expected = (
        """shared |context context \n0:-0.0:1.0 |action1 0 \n|action1 1 \n|action1 2 """
    )
    selected = pick_best_chain.PickBest.Selected(index=0, probability=1.0, score=0.0)
    event = pick_best_chain.PickBest.Event(
        inputs={},
        to_select_from=named_actions,
        based_on={"context": "context"},
        selected=selected,
    )
    vw_ex_str = text_embedder.to_vw_format(event)
    assert vw_ex_str == expected


def test_pickbest_textembedder_w_full_label_w_emb():
    text_embedder = pick_best_chain.PickBestTextEmbedder(model=MockEncoder())
    str1 = "0"
    str2 = "1"
    str3 = "2"
    encoded_str1 = encoded_text + " ".join(char for char in str1)
    encoded_str2 = encoded_text + " ".join(char for char in str2)
    encoded_str3 = encoded_text + " ".join(char for char in str3)

    ctx_str_1 = "context1"
    encoded_ctx_str_1 = encoded_text + " ".join(char for char in ctx_str_1)

    named_actions = {"action1": pick_best_chain.base.Embed([str1, str2, str3])}
    context = {"context": pick_best_chain.base.Embed(ctx_str_1)}
    expected = f"""shared |context {encoded_ctx_str_1} \n0:-0.0:1.0 |action1 {encoded_str1} \n|action1 {encoded_str2} \n|action1 {encoded_str3} """
    selected = pick_best_chain.PickBest.Selected(index=0, probability=1.0, score=0.0)
    event = pick_best_chain.PickBest.Event(
        inputs={}, to_select_from=named_actions, based_on=context, selected=selected
    )
    vw_ex_str = text_embedder.to_vw_format(event)
    assert vw_ex_str == expected


def test_pickbest_textembedder_more_namespaces_no_label_no_emb():
    text_embedder = pick_best_chain.PickBestTextEmbedder(model=MockEncoder())
    named_actions = {"action1": [{"a": "0", "b": "0"}, "1", "2"]}
    context = {"context1": "context1", "context2": "context2"}
    expected = """shared |context1 context1 |context2 context2 \n|a 0 |b 0 \n|action1 1 \n|action1 2 """
    event = pick_best_chain.PickBest.Event(
        inputs={}, to_select_from=named_actions, based_on=context
    )
    vw_ex_str = text_embedder.to_vw_format(event)
    assert vw_ex_str == expected


def test_pickbest_textembedder_more_namespaces_w_label_no_emb():
    text_embedder = pick_best_chain.PickBestTextEmbedder(model=MockEncoder())
    named_actions = {"action1": [{"a": "0", "b": "0"}, "1", "2"]}
    context = {"context1": "context1", "context2": "context2"}
    expected = """shared |context1 context1 |context2 context2 \n|a 0 |b 0 \n|action1 1 \n|action1 2 """
    selected = pick_best_chain.PickBest.Selected(index=0, probability=1.0)
    event = pick_best_chain.PickBest.Event(
        inputs={}, to_select_from=named_actions, based_on=context, selected=selected
    )
    vw_ex_str = text_embedder.to_vw_format(event)
    assert vw_ex_str == expected


def test_pickbest_textembedder_more_namespaces_w_full_label_no_emb():
    text_embedder = pick_best_chain.PickBestTextEmbedder(model=MockEncoder())
    named_actions = {"action1": [{"a": "0", "b": "0"}, "1", "2"]}
    context = {"context1": "context1", "context2": "context2"}
    expected = """shared |context1 context1 |context2 context2 \n0:-0.0:1.0 |a 0 |b 0 \n|action1 1 \n|action1 2 """
    selected = pick_best_chain.PickBest.Selected(index=0, probability=1.0, score=0.0)
    event = pick_best_chain.PickBest.Event(
        inputs={}, to_select_from=named_actions, based_on=context, selected=selected
    )
    vw_ex_str = text_embedder.to_vw_format(event)
    assert vw_ex_str == expected


def test_pickbest_textembedder_more_namespaces_w_full_label_w_full_emb():
    text_embedder = pick_best_chain.PickBestTextEmbedder(model=MockEncoder())

    str1 = "0"
    str2 = "1"
    str3 = "2"
    encoded_str1 = encoded_text + " ".join(char for char in str1)
    encoded_str2 = encoded_text + " ".join(char for char in str2)
    encoded_str3 = encoded_text + " ".join(char for char in str3)

    ctx_str_1 = "context1"
    ctx_str_2 = "context2"
    encoded_ctx_str_1 = encoded_text + " ".join(char for char in ctx_str_1)
    encoded_ctx_str_2 = encoded_text + " ".join(char for char in ctx_str_2)

    named_actions = {
        "action1": pick_best_chain.base.Embed([{"a": str1, "b": str1}, str2, str3])
    }
    context = {
        "context1": pick_best_chain.base.Embed(ctx_str_1),
        "context2": pick_best_chain.base.Embed(ctx_str_2),
    }
    expected = f"""shared |context1 {encoded_ctx_str_1} |context2 {encoded_ctx_str_2} \n0:-0.0:1.0 |a {encoded_str1} |b {encoded_str1} \n|action1 {encoded_str2} \n|action1 {encoded_str3} """

    selected = pick_best_chain.PickBest.Selected(index=0, probability=1.0, score=0.0)
    event = pick_best_chain.PickBest.Event(
        inputs={}, to_select_from=named_actions, based_on=context, selected=selected
    )
    vw_ex_str = text_embedder.to_vw_format(event)
    assert vw_ex_str == expected


def test_pickbest_textembedder_more_namespaces_w_full_label_w_partial_emb():
    text_embedder = pick_best_chain.PickBestTextEmbedder(model=MockEncoder())

    str1 = "0"
    str2 = "1"
    str3 = "2"
    encoded_str1 = encoded_text + " ".join(char for char in str1)
    encoded_str2 = encoded_text + " ".join(char for char in str2)
    encoded_str3 = encoded_text + " ".join(char for char in str3)

    ctx_str_1 = "context1"
    ctx_str_2 = "context2"
    encoded_ctx_str_1 = encoded_text + " ".join(char for char in ctx_str_1)
    encoded_ctx_str_2 = encoded_text + " ".join(char for char in ctx_str_2)

    named_actions = {
        "action1": [
            {"a": str1, "b": pick_best_chain.base.Embed(str1)},
            str2,
            pick_best_chain.base.Embed(str3),
        ]
    }
    context = {"context1": ctx_str_1, "context2": pick_best_chain.base.Embed(ctx_str_2)}
    expected = f"""shared |context1 {ctx_str_1} |context2 {encoded_ctx_str_2} \n0:-0.0:1.0 |a {str1} |b {encoded_str1} \n|action1 {str2} \n|action1 {encoded_str3} """

    selected = pick_best_chain.PickBest.Selected(index=0, probability=1.0, score=0.0)
    event = pick_best_chain.PickBest.Event(
        inputs={}, to_select_from=named_actions, based_on=context, selected=selected
    )
    vw_ex_str = text_embedder.to_vw_format(event)
    assert vw_ex_str == expected
