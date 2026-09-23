/**
 * ShorelineDT minimal public GAMA contract demonstration.
 *
 * Run `python scripts/demo/run_demo.py` before launching the experiment.
 * The generated values are synthetic and are not observations, forecasts, or
 * management recommendations for a real coast.
 */
model ShorelineDT_demo

global {
    string contract_path <- "../output/demo/gama_contract.csv";

    init {
        matrix contract <- matrix(csv_file(contract_path, ","));
        int row_count <- length(rows_list(contract));
        loop i from: 0 to: row_count - 1 {
            create decision_unit number: 1 {
                unit_id <- int(contract[0, i]);
                retreat_m <- float(contract[1, i]);
                uncertainty_m <- float(contract[2, i]);
                dbvr <- float(contract[3, i]);
                poe <- float(contract[4, i]);
                priority_code <- int(contract[5, i]);
                action_code <- int(contract[6, i]);
                volume_m3 <- float(contract[7, i]);
                location <- {float(unit_id) * 10.0, 50.0};
            }
        }
        write "Loaded " + length(decision_unit) + " synthetic decision units.";
    }
}

species decision_unit {
    int unit_id;
    float retreat_m;
    float uncertainty_m;
    float dbvr;
    float poe;
    int priority_code;
    int action_code;
    float volume_m3;

    aspect default {
        draw circle(2.5) color:
            priority_code = 1 ? #red :
            (priority_code = 2 ? #orange :
            (priority_code = 3 ? #yellow : #green));
    }
}

experiment ShorelineDT_Public_Demo type: gui {
    output {
        display "Synthetic uncertainty-to-decision contract" {
            species decision_unit aspect: default;
        }
    }
}
