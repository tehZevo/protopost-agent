# Protopost Agent

Protopost as tools. Protopost as agent that uses Protopost tools. Yes. Very nice.

The agent can run in one of three modes:
- Interactive (default): Interact with the agent and its Protopost tools via your shell
- Service (`-s`): Start a Protopost server that hosts your agent
- Autonomous (`-a`): Run agent autonomously, optionally in a loop

### How do?
0. Set up Ollama
1. Run `pip install git+https://github.com/tehzevo/protopost-agent.git#egg=protopost`
2. Create `config.yaml` (see examples)
3. Run `protopost-agent` (or add `--help`)
