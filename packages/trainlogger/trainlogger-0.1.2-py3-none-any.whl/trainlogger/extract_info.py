import os
from glob import glob

import pandas as pd
import tensorflow as tf


def from_markdown(string: str) -> str:
    """
    Formats linebreaks and indentation from Markdown format to python format.
    Replaces "&nbsp;&nbsp;"  with " ".
    Replaces "<br />" with "\n".
    """
    if string is not None:
        formatted_string = string.replace("&nbsp;&nbsp;", " ").replace("<br />", "\n")
    else:
        formatted_string = "None"
    return formatted_string


def parse_tf_event(tf_event):
    """
    Parses a given tf event by extracting the
        - wall_time
        - name
        - step
        - value
    of this event and returns it as a dict.
    """
    infos = {
        "wall_time": tf_event.wall_time,
        "name": tf_event.summary.value[0].tag,
        "step": tf_event.step,
    }
    if tf_event.summary.value[0].tag.endswith("text_summary"):
        # noinspection PyTypedDict
        infos["value"] = from_markdown(tf_event.summary.value[0].tensor.string_val[0].decode("utf-8"))
    else:
        infos["value"] = float(tf_event.summary.value[0].simple_value),
    return infos


def get_tf_events_df(tf_file):
    """
    Combines all events of a tf event file into one dataframe and returns it.
    """
    df = pd.DataFrame([parse_tf_event(e) for e in tf.compat.v1.train.summary_iterator(tf_file) if len(e.summary.value)])
    return df


def get_tf_file_path(dir_path):
    """
    Searches for a tf event file in the given directory.
    Returns its path if only one is found.
    Raises an error if none or more than one are found.
    """
    potential_paths = glob(os.path.join(dir_path, "events.out.*"))
    if len(potential_paths) != 1:
        raise LookupError("No or file or more than one file found!")
    else:
        return potential_paths[0]


def compare_score_of_runs(list_of_runs):
    """
    Extracts all final scores of the given runs and returns them as a dict.
    """
    scores = {}
    for dir_path in list_of_runs:
        # dir_path = os.path.join(constants.ROOT, run)
        tf_file = get_tf_file_path(dir_path)
        tf_df = get_tf_events_df(tf_file)
        info = tf_df.loc[tf_df["name"] == "Score/text_summary", "value"]

        if len(info) == 1:
            scores[run] = float(info.item())
        else:
            scores[run] = "No or file or more than one value found!"

    return scores


def get_comparison_of_runs(list_of_runs):
    """
    Extracts all information of the given runs and returns a combined dataframe.
    """
    run_dfs = []
    for dir_path in list_of_runs:
        # dir_path = os.path.join(constants.ROOT, run)
        tf_file = get_tf_file_path(dir_path)
        tf_df = get_tf_events_df(tf_file)
        tf_df["run"] = run
        run_dfs.append(tf_df)

    combined_df = pd.concat(run_dfs)

    return combined_df


if __name__ == "__main__":
    runs = [
        "runs/local/3to1_image",
        "runs/local/1to1_image"
    ]

    print(compare_score_of_runs(runs))
