import random
from Animacoes.terminalAnimation import terminalAnimation
from Animacoes.jumpscare import foxy
from Animacoes.running_skele import yallsee

_registry: dict = {}

def register_animation(func, weight: float = 1.0):
  _registry[func] = float(weight)


def unregister_animation(func):
  _registry.pop(func, None)


def list_registered():
  return dict(_registry)

register_animation(terminalAnimation, weight=1000.0)
register_animation(foxy, weight=10.0)
register_animation(yallsee, weight=10.0)


def choose_animation(override_weights: dict | None = None):
  source = override_weights if override_weights is not None else _registry
  if not source:
    raise RuntimeError("No animations registered")

  funcs = list(source.keys())
  weights = [float(source[f]) for f in funcs]
  return random.choices(funcs, weights=weights, k=1)[0]
