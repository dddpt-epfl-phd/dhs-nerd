from csv import DictReader
import os

from IPython.display import Javascript, display



pred_true_comparator_dir_path = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(pred_true_comparator_dir_path, "PredTrueComparator.js")) as jsfile:
    pred_true_comparator_js_content = jsfile.read()
with open(os.path.join(pred_true_comparator_dir_path, "PredTrueComparator.css")) as jsfile:
    pred_true_comparator_css_content = jsfile.read().replace("\n", "")
css_string_var_declaration = f"var CSS_AS_STRING = '{pred_true_comparator_css_content}'\n\n" 

def clef_hipe_load_conllu_tsv_to_dict(filepath):
    with open(filepath) as csvfile:
        conllu_tsv = [r for r in DictReader(csvfile, delimiter="\t")]
    conllu_tsv = [r for r in conllu_tsv if len(r["TOKEN"])!=0 and not r["TOKEN"].startswith("#")]
    return conllu_tsv



def compare_pred_true(pred_conllu, true_conllu, text_property, compare_property, separatorsProperty, properties_to_display):
    for p in pred_conllu:
        p["text"] = p[text_property]
    for t in true_conllu:
        t["text"] = t[text_property]
    predstr = str(pred_conllu).replace("\n", "")
    truestr = str(true_conllu).replace("\n", "")
    properties_to_display_str = str(properties_to_display).replace("\n", "")
    jsCode = css_string_var_declaration+pred_true_comparator_js_content+f'''
    element.append(visualizePredTrueComparison({predstr}, {truestr}, "{compare_property}", "{separatorsProperty}", {properties_to_display_str}))'''
    display(Javascript(
        jsCode
    ))
