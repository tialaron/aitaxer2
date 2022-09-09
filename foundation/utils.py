# Copyright (c) 2020, salesforce.com, inc.
# All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# For full license text, see the LICENSE file in the repo root
# or https://opensource.org/licenses/BSD-3-Clause

import json
import os
import sys
import numpy as np
from hashlib import sha512

import lz4.frame
from Crypto.PublicKey import RSA

#from ai_economist.foundation.base.base_env import BaseEnvironment
from base_env import BaseEnvironment

def save_episode_log(game_object, filepath, compression_level=16):
    """Save a lz4 compressed version of the dense log stored
    in the provided game object"""
    assert isinstance(game_object, BaseEnvironment)
    compression_level = int(compression_level)
    if compression_level < 0:
        compression_level = 0
    elif compression_level > 16:
        compression_level = 16

    with lz4.frame.open(
        filepath, mode="wb", compression_level=compression_level
    ) as log_file:
        log_bytes = bytes(
            json.dumps(
                game_object.previous_episode_dense_log, ensure_ascii=False
            ).encode("utf-8")
        )
        log_file.write(log_bytes)


def load_episode_log(filepath):
    """Load the dense log saved at provided filepath"""
    with lz4.frame.open(filepath, mode="rb") as log_file:
        log_bytes = log_file.read()
    return json.loads(log_bytes)


def verify_activation_code():
    """
    Validate the user's activation code.
    If the activation code is valid, also save it in a text file for future reference.
    If the activation code is invalid, simply exit the program
    """
    path_to_activation_code_dir = os.path.dirname(os.path.abspath(__file__))

    def validate_activation_code(code, msg=b"covid19 code activation"):
        filepath = os.path.abspath(
            os.path.join(
                path_to_activation_code_dir,
                "scenarios/covid19/key_to_check_activation_code_against",
            )
        )
        with open(filepath, "r") as fp:
            key_pair = RSA.import_key(fp.read())

        hashed_msg = int.from_bytes(sha512(msg).digest(), byteorder="big")
        signature = pow(hashed_msg, key_pair.d, key_pair.n)
        try:
            exp_from_code = int(code, 16)
            hashed_msg_from_signature = pow(signature, exp_from_code, key_pair.n)

            return hashed_msg == hashed_msg_from_signature
        except ValueError:
            return False

    activation_code_filename = "activation_code.txt"

    filepath = os.path.join(path_to_activation_code_dir, activation_code_filename)
    if activation_code_filename in os.listdir(path_to_activation_code_dir):
        print("Using the activation code already present in '{}'".format(filepath))
        with open(filepath, "r") as fp:
            activation_code = fp.read()
            fp.close()
        if validate_activation_code(activation_code):
            return  # already activated
        print(
            "The activation code saved in '{}' is incorrect! "
            "Please correct the activation code and try again.".format(filepath)
        )
        sys.exit(0)
    else:
        print(
            "In order to run this simulation, you will need an activation code.\n"
            "Please fill out the form at "
            "https://forms.gle/dJ2gKDBqLDko1g7m7 and we will send you an "
            "activation code to the provided email address.\n"
        )
        num_attempts = 5
        attempt_num = 0
        while attempt_num < num_attempts:
            activation_code = input(
                f"Whenever you are ready, "
                "please enter the activation code: "
                f"(attempt {attempt_num + 1} / {num_attempts})"
            )
            attempt_num += 1
            if validate_activation_code(activation_code):
                print(
                    "Saving the activation code in '{}' for future "
                    "use.".format(filepath)
                )
                with open(
                    os.path.join(path_to_activation_code_dir, activation_code_filename),
                    "w",
                ) as fp:
                    fp.write(activation_code)
                    fp.close()
                return
            print("Incorrect activation code. Please try again.")
        print(
            "You have had {} attempts to provide the activate code. Unfortunately, "
            "none of the activation code(s) you provided could be validated. "
            "Exiting...".format(num_attempts)
        )
        sys.exit(0)


def annealed_tax_limit(completions, warmup_period, slope, final_max_tax_value=1.0):
    """
    Compute the maximum tax rate available at this stage of tax annealing.

    This function uses the number of episode completions and the annealing schedule
    (warmup_period, slope, & final_max_tax_value) to determine what the maximum tax
    rate can be.
    This type of annealing allows for a tax curriculum where earlier episodes are
    restricted to lower tax rates. As more episodes are played, higher tax values are
    allowed.

    Args:
        completions (int): Number of times the environment has completed an episode.
            Expected to be >= 0.
        warmup_period (int): Until warmup_period completions, only allow 0 tax. Using
            a negative value will enable non-0 taxes at 0 environment completions.
        slope (float): After warmup_period completions, percentage of full tax value
            unmasked with each new completion.
        final_max_tax_value (float): The maximum tax value at the end of annealing.

    Returns:
        A scalar value indicating the maximum tax at this stage of annealing.

    Example:
        >> WARMUP = 100
        >> SLOPE = 0.01
        >> annealed_tax_limit(0, WARMUP, SLOPE)
        0.0
        >> annealed_tax_limit(100, WARMUP, SLOPE)
        0.0
        >> annealed_tax_limit(150, WARMUP, SLOPE)
        0.5
        >> annealed_tax_limit(200, WARMUP, SLOPE)
        1.0
        >> annealed_tax_limit(1000, WARMUP, SLOPE)
        1.0
    """
    # What percentage of the full range is currently visible
    # (between 0 [only 0 tax] and 1 [all taxes visible])
    percentage_visible = np.maximum(
        0.0, np.minimum(1.0, slope * (completions - warmup_period))
    )

    # Determine the highest allowable tax,
    # given the current position in the annealing schedule
    current_max_tax = percentage_visible * final_max_tax_value

    return current_max_tax


def annealed_tax_mask(completions, warmup_period, slope, tax_values):
    """
    Generate a mask applied to a set of tax values for the purpose of tax annealing.

    This function uses the number of episode completions and the annealing schedule
    to determine which of the tax values are considered valid. The most extreme
    tax/subsidy values are unmasked last. Zero tax is always unmasked (i.e. always
    valid).
    This type of annealing allows for a tax curriculum where earlier episodes are
    restricted to lower tax rates. As more episodes are played, higher tax values are
    allowed.

    Args:
        completions (int): Number of times the environment has completed an episode.
            Expected to be >= 0.
        warmup_period (int): Until warmup_period completions, only allow 0 tax. Using
            a negative value will enable non-0 taxes at 0 environment completions.
        slope (float): After warmup_period completions, percentage of full tax value
            unmasked with each new completion.
        tax_values (list): The list of tax values associated with each action to
            which this mask will apply.

    Returns:
        A binary mask with same shape as tax_values, indicating which tax values are
            currently valid.

    Example:
        >> WARMUP = 100
        >> SLOPE = 0.01
        >> TAX_VALUES = [0.0, 0.25, 0.50, 0.75, 1.0]
        >> annealed_tax_limit(0, WARMUP, SLOPE, TAX_VALUES)
        [0, 0, 0, 0, 0]
        >> annealed_tax_limit(100, WARMUP, SLOPE, TAX_VALUES)
        [0, 0, 0, 0, 0]
        >> annealed_tax_limit(150, WARMUP, SLOPE, TAX_VALUES)
        [1, 1, 1, 0, 0]
        >> annealed_tax_limit(200, WARMUP, SLOPE, TAX_VALUES)
        [1, 1, 1, 1, 1]
        >> annealed_tax_limit(1000, WARMUP, SLOPE, TAX_VALUES)
        [1, 1, 1, 1, 1]
    """
    # Infer the most extreme tax level from the supplied tax values.
    abs_tax = np.abs(tax_values)
    full_tax_amount = np.max(abs_tax)

    # Determine the highest allowable tax, given the current position
    # in the annealing schedule
    max_absolute_visible_tax = annealed_tax_limit(
        completions, warmup_period, slope, full_tax_amount
    )

    # Return a binary mask to allow for taxes
    # at or below the highest absolute visible tax
    return np.less_equal(np.abs(tax_values), max_absolute_visible_tax).astype(
        np.float32
    )
