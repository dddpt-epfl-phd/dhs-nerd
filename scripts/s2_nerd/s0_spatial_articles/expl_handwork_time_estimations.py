# %%

from s1_entities_to_extract_list import *
# %%

# %%

relationship_nb_estimation_low = [
    (10, 3),
    (20, 3),
    (30, 3),
    (40, 2),
]

relationship_nb_estimation_mid = [
    (10, 5),
    (20, 3),
    (30, 3),
    (40, 2),
]

relationship_nb_estimation_high = [
    (10, 6),
    (20, 5),
    (30, 4),
    (40, 3),
]

relationship_nb_estimations = [
    ("nb_rel_low", relationship_nb_estimation_low),
    ("nb_rel_mid", relationship_nb_estimation_mid),
    ("nb_rel_high", relationship_nb_estimation_high)
]

# Estimation rules for relationships
def relationship_nb_estimator(lvl, relationship_nb_estimation):
    for threshold, nb_relationships in relationship_nb_estimation:
        if lvl<=threshold:
            return nb_relationships

def add_nb_rel_estimation_to_dtf(dtf, col_name, relationship_nb_estimation):
    dtf[col_name] = [r[1].nb_articles * relationship_nb_estimator(r[0], relationship_nb_estimation)  for r in dtf.iterrows()]
def add_nb_rel_estimations_to_dtf(dtf, estimations):
    for col_name, estimation in estimations:
        add_nb_rel_estimation_to_dtf(dtf, col_name, estimation)
    
add_nb_rel_estimations_to_dtf(selected_tags_by_lvl, relationship_nb_estimations)
selected_tags_by_lvl
# %%
nb_things_to_extract = selected_tags_by_lvl.aggregate(sum).to_frame("nb_things")
# -> ~20k relations to extract, gargl...
nb_things_to_extract
# %%

"""
Now let's go to time-estimations:
"""

minutes_per_entity ={
    "low": 5,
    "mid": 10,
    "high": 20
}
minutes_per_relation ={
    "low": 5,
    "mid": 10,
    "high": 20
}

def add_time_estimation(dtf, est_lvl_ent, est_lvl_rel):
    colname_basis = "rel"+est_lvl_rel+"_ent"+est_lvl_ent
    colname_h = colname_basis+"_h"
    colname_d = colname_basis+"_d"
    colname_wy = colname_basis+"_wy"
    dtf[colname_h] = minutes_per_relation[est_lvl_rel]*dtf.nb_things / 60
    dtf[colname_h][0] = dtf.nb_things[0] * minutes_per_entity[est_lvl_ent] / 60
    dtf[colname_h][1:] +=dtf[colname_h][0]
    dtf[colname_d] = dtf[colname_h] / 8
    dtf[colname_wy] = dtf[colname_d] / 200
    dtf = dtf.round(1)
    return dtf

nb_things_to_extract = add_time_estimation(nb_things_to_extract,"low","low")
nb_things_to_extract = add_time_estimation(nb_things_to_extract,"mid","mid")
nb_things_to_extract = add_time_estimation(nb_things_to_extract,"high","high")

nb_things_to_extract
