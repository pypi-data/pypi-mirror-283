# Copyright 2024 BDP Ecosystem Limited. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

import brainstate as bst
import brainunit as bu
import jax

__all__ = [
  'State4Integral',
  'euler_step',
  'rk2_step',
  'rk3_step',
  'rk4_step',
]


class State4Integral(bst.ShortTermState):
  """
  A state that integrates the state of the system to the integral of the state.
  """
  pass


def tree_map(f, tree, *rest):
  return jax.tree.map(f, tree, *rest, is_leaf=lambda a: isinstance(a, bu.Quantity))



def euler_step(target, t: jax.typing.ArrayLike, *args):
  with bst.environ.context(t=t):
    return target(*args)


def rk2_step(target, t: jax.typing.ArrayLike, *args):
  dt = bst.environ.get_dt()

  # k1
  with bst.environ.context(t=t):
    with bst.StateTrace() as trace:
      target(*args)

      # state collection
      states = tuple(trace.states)
      for st in states:
        assert isinstance(st, State4Integral), f"Only State4Integral is supported currently: {st}"

      # value collection
      ys = list(trace._org_values)
      k1hs = [st.value for st in states]

  # k2
  with bst.environ.context(t=t + dt):
    for st, y, k1h in zip(states, ys, k1hs):
      st.value = tree_map(lambda y_, k1_: y_ + k1_, y, k1h)
    target(*args)
    k2s = [st.value for st in states]

  # y + (k1 + k2) / 2
  for st, y, k1h, k2h in zip(states, ys, k1hs, k2s):
    st.value = tree_map(lambda y_, k1_, k2_: y_ + 0.5 * (k1_ + k2_), y, k1h, k2h)


def rk3_step(target, t: jax.typing.ArrayLike, *args):
  dt = bst.environ.get_dt()

  # k1
  with bst.environ.context(t=t):
    with bst.StateTrace() as trace:
      target(*args)

      # state collection
      states = tuple(trace.states)
      for st in states:
        assert isinstance(st, State4Integral), f"Only State4Integral is supported currently: {st}"

      # value collection
      ys = list(trace._org_values)
      k1hs = [st.value for st in states]

  # k2
  with bst.environ.context(t=t + dt * 0.5):
    for st, y, k1h in zip(states, ys, k1hs):
      st.value = tree_map(lambda y_, k1_: y_ + k1_ * 0.5, y, k1h)
    target(*args)
    k2hs = [st.value for st in states]

  # k3
  with bst.environ.context(t=t + dt * 0.5):
    for st, y, k2h in zip(states, ys, k2hs):
      st.value = tree_map(lambda y_, k2_: y_ + k2_ * 0.5, y, k2h)
    target(*args)
    k3hs = [st.value for st in states]

  # y + (k1 + 4 * k2 + k3) / 2
  for st, y, k1h, k2h, k3h in zip(states, ys, k1hs, k2hs, k3hs):
    st.value = tree_map(lambda y_, k1_, k2_, k3_: y_ + (k1_ + 4 * k2_ + k3_) / 6, y, k1h, k2h, k3h)


def rk4_step(target, t: jax.typing.ArrayLike, *args):
  dt = bst.environ.get_dt()

  # k1
  with bst.environ.context(t=t):
    with bst.StateTrace() as trace:
      target(*args)

    # state collection
    states = tuple(trace.states)
    for st in states:
      assert isinstance(st, State4Integral), f"Only State4Integral is supported currently: {st}"

    # value collection
    ys = list(trace._org_values)
    k1hs = [st.value for st in states]

  # k2
  with bst.environ.context(t=t + 0.5 * dt):
    for st, y, k1h in zip(states, ys, k1hs):
      st.value = tree_map(lambda y_, k1_: y_ + 0.5 * k1_, y, k1h)
    target(*args)
    k2hs = [st.value for st in states]

  # k3
  with bst.environ.context(t=t + 0.5 * dt):
    for st, y, k2h in zip(states, ys, k2hs):
      st.value = tree_map(lambda y_, k2_: y_ + 0.5 * k2_, y, k2h)
    target(*args)
    k3hs = [st.value for st in states]

  # k4
  with bst.environ.context(t=t + dt):
    for st, y, k3h in zip(states, ys, k3hs):
      st.value = tree_map(lambda y_, k3_: y_ + k3_, y, k3h)
    target(*args)
    k4hs = [st.value for st in states]

  # y + (k1 + 2 * k2 + 2 * k3 + k4) / 6
  for st, y, k1h, k2h, k3h, k4h in zip(states, ys, k1hs, k2hs, k3hs, k4hs):
    st.value = tree_map(lambda y_, k1_, k2_, k3_, k4_: y_ + (k1_ + 2 * k2_ + 2 * k3_ + k4_) / 6,
                        y, k1h, k2h, k3h, k4h)
