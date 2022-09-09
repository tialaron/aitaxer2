# Copyright (c) 2020, salesforce.com, inc.
# All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# For full license text, see the LICENSE file in the repo root
# or https://opensource.org/licenses/BSD-3-Clause

#from foundation.base.base_agent import agent_registry
from base_agent import agent_registry
from base_component import component_registry
#from . import mobiles, planners

#from ai_economist.foundation.base.base_component import component_registry

#from . import ( build,  continuous_double_auction,    covid19_components, move, redistribution, simple_labor)

#from ai_economist.foundation.base.base_env import scenario_registry
from base_env import scenario_registry

#from .covid19 import covid19_env
#from .one_step_economy import one_step_economy
#from .simple_wood_and_stone import dynamic_layout, layout_from_file

#from .endogenous import endogenous_registry
#from .landmarks import landmark_registry
#from .resources import resource_registry

#from ai_economist.foundation import utils
#from ai_economist.foundation.agents import agent_registry as agents
#from ai_economist.foundation.components import component_registry as components
#from ai_economist.foundation.entities import endogenous_registry as endogenous
#from ai_economist.foundation.entities import landmark_registry as landmarks
#from ai_economist.foundation.entities import resource_registry as resources
#from ai_economist.foundation.scenarios import scenario_registry as scenarios
import utils
from base_agent import agent_registry as agents
from base_component import component_registry as components
import one_step_economy
import dynamic_layout, layout_from_file
from endogenous import endogenous_registry
from landmarks import landmark_registry
from resources import resource_registry

def make_env_instance(scenario_name, **kwargs):
    scenario_class = scenarios.get(scenario_name)
    return scenario_class(**kwargs)

