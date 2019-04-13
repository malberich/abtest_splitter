import scipy
from statsmodels.stats.proportion import proportions_ztest
import requests
import time

if __name__ == '__main__':
    total_assignments = {}

    r = requests.get("http://127.0.0.1:5000/experiments/")
    experiment_list = r.json()
    experiments = dict(
        (group['key'], group) for group in experiment_list
    )

    start_time = time.time()
    for i in range(1, 100000):
        r = requests.get("http://127.0.0.1:5000/splits/{}".format(i))
        assignments = r.json()
        for idx, assignment in enumerate(assignments):
            # print(idx, assignment)
            if assignment['experiment_id'] not in total_assignments.keys():
                total_assignments[assignment['experiment_id']] = {}
            # print(
            #     assignment['group_name']['key'],
            #     total_assignments[
            #         assignment['experiment_id']
            #     ].get(
            #         assignment['group_name']['key'],
            #         0
            #     )
            # )
            total_assignments[
                assignment['experiment_id']
            ][assignment['group_name']['key']] = total_assignments[
                assignment['experiment_id']
            ].get(assignment['group_name']['key'], 0) + 1

        # print(total_assignments)

        if i % 1000 == 0 and i > 0:
            print("{}: {:.4f}".format(i, i / (time.time() - start_time)))
            print(total_assignments)

            for (experiment, assignments) in total_assignments.items():
                exp_audience = experiments.get(
                    experiment,
                    {'audience': 100}
                )['audience']
                group_sizes = experiments.get(
                    experiment,
                    {
                        'groups': [
                            {
                                'key': 'Control',
                                'size': 100
                            }
                        ]
                    }
                )['groups']
                total_evaluations = sum(assignments.values())
                percent_keys = dict(
                    (group_name, float(value) / float(total_evaluations))
                    for (group_name, value) in assignments.items()
                )
                expected_percents = dict(
                    (
                        group['key'],
                        (float(group['size']) / 100.0) * (exp_audience / 100.0)
                    )
                    for group in group_sizes
                )

                expected_percents['(Excluded)'] = 1.0 - exp_audience / 100.0
                # print(percent_keys)
                # print(assignments.values())
                # print(expected_percents.values())
                # print(
                #     [
                #         total_evaluations for i in percent_keys.keys()
                #     ]
                # )

                for k in percent_keys.keys():
                    if '(Excluded)' in k:
                        expected = expected_percents[k]
                        nobs = total_evaluations
                        zstat, p_vals = proportions_ztest(
                            assignments[k],
                            nobs,
                            value=expected
                        )
                    else:
                        expected = expected_percents[k] / (exp_audience / 100.0)
                        nobs = total_evaluations - assignments['(Excluded)']
                        zstat, p_vals = proportions_ztest(
                            assignments[k],
                            nobs,
                            value=expected
                        )
                    print(
                        "{}: x={}, obs={}, p={:.4f}, exp={}, p-val={:.5f}".format(
                            k,
                            assignments[k],
                            nobs,
                            assignments[k] / nobs,
                            expected,
                            p_vals
                        )
                    )

