from swiftllm import OpenAI


def test_constructor():
    model = OpenAI(instructions='Help me troubleshoot the API I am using to talk to you by having a conversation with me.')
    assert model.instructions == 'SYSTEM INSTRUCTIONS:\nHelp me troubleshoot the API I am using to talk to you by having a conversation with me.'
    assert model.schema == {}
    assert model.sample_outputs == []
    assert isinstance(model, OpenAI)

test_constructor()