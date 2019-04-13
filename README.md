## Introduction

This is a proof-of-concept for a HTTP endpoint that randomly splits users based on a seed string. Its main purpose is to simulate A/B testing user assignments (user splits), and also to perform tests on the statistical properties of the split algorithm.

The random split decision is taken from a simple SHA1 digest calculation. The random seed is based on the experiment name and the user-id as sent through the HTTP request.

The app includes the following features:
* allows to set multiple tests
* each group can have two or more groups
* The sizes of each group can vary (although the most usual is that they all have the same size).
* Each experiment can limit the % of the total candidate users that will be eligible for the test.

## Experiment configuration

The Flask application loads the experiments from the experiments.yaml file (make a copy of the experiments.dist.yaml in the same folder and rename it).

### Configuring an experiment

The following is a sample section in the dist file for an A/B test:

```yaml
experiments
  - key: Sample A/B test
    audience: 25
    status: 1
    groups:
      - key: "Control"
        size: 50
      - key: "Variant"
        size: 50
```

The most important elements are:

* key: should be unique for all the experiments.
* audience: optional (by default 100) tells how many users are chosen for the experiment.
* status: 0=stopped, 1=running
* groups: a list including all the potential containers of the users in the test.
  * key: Unique string in the experiment that identifies the group.
  * size: Number representing the percent users in the test that should fall into this group.

At this current version the algorithm is so naive that it does not even check if the groups add up to 100, which means that you can plainly ignore the audience and set the direct percents in the same groups.

### Buckets: Special randomization groups

Whenever we need a second- or even third-level split for any experiment we could use the buckets. The buckets essentially work as randomized groupings that potentially should be stochastically independent from each other and from the experiments.

The default configuration MUST include one special bucket: the audience. In order to decide whether to assign a given user to a given audience level, the app applies the same randomization procedure to assign any user to any given audience level. The bucket generates 100 groups and if the user's group is lower than the current audience, the user is eligible for the group.

### Other configurations

Another important configuration deals with the value that should be assigned to a member that is excluded from a test.

## Downloading and running the app

Clone the repository, create the virtual environment and install the requirements

```shell
$ git clone https://github.com/malberich/abtest_splitter.git .

...

$ cd abtest_splitter
$ virtualenv -p python3 --site-system-packages ./venv
...
$ pip install -r requirements.txt
...
```

Now your environment should be ready to run the app.

Copy the experiments.dist.yaml:

```shell
$ cd conf/
$ cp experiments.dist.yaml experiments.yaml
```

Now edit the configuration in the YAML file and run the app:

```shell
$ FLASK_APP=splitter/run.py FLASK_DEBUG=1 python -m flask run
```

It should be available at http://localhost:5000/

You can now make a request to see the list of active experiments:

```shell
$ curl http://localhost:5000/experiments/
```

which should return something similar to what is stored in the ```experiments.yaml``` file:

```json
[
  {
    "audience": 25,
    "groups": [
      {
        "key": "Control",
        "size": 50
      },
      {
        "key": "Variant",
        "size": 50
      }
    ],
    "key": "Sample A/B test",
    "status": 1
  }
]
```

Now that we can see the available experiments, you can try to assign a user with id=12345. You can do so by performing the following request:

```shell
$ curl http://localhost:5000/splits/4000
```

which should return something similar to:

```json
[
  {
    "experiment_id": "Sample A/B test",
    "group": 0,
    "group_name": "Control"
  }
]
```

## Examples and use cases

The /examples/ folder include a few cases that expose situations where the splitter can be used. Only one of them connects through the HTTP endpoints, while the others execute the split procedure through a CLI command.

The combination of both cases allows to use this simple tool both in the backend and frontend sides.

### HTTP example: 100,000 random splits

The script goes through a loop and splits the users for all the tests that have been configured in the experiments.yaml file and returns a json containing the user assignment to each experiment.

This example also includes a significance test verification to check that the splits have an statistically expected value depending on the sample size. The significance test is run every 1000 samples and allows to see an output similar to the one below:

```shell
95000: 304.1695
{'Sample A/B test': {'Control': 11940, '(Excluded)': 71090, 'Variant': 11970}}
Control: x=11940, obs=23910, p=0.4994, exp=0.5, p-val=0.84617
(Excluded): x=71090, obs=95000, p=0.7483, exp=0.75, p-val=0.23164
Variant: x=11970, obs=23910, p=0.5006, exp=0.5, p-val=0.84617
96000: 303.9503
{'Sample A/B test': {'Control': 12088, '(Excluded)': 71835, 'Variant': 12077}}
Control: x=12088, obs=24165, p=0.5002, exp=0.5, p-val=0.94359
(Excluded): x=71835, obs=96000, p=0.7483, exp=0.75, p-val=0.21981
Variant: x=12077, obs=24165, p=0.4998, exp=0.5, p-val=0.94359
97000: 304.1832
{'Sample A/B test': {'Control': 12236, '(Excluded)': 72575, 'Variant': 12189}}
Control: x=12236, obs=24425, p=0.5010, exp=0.5, p-val=0.76362
(Excluded): x=72575, obs=97000, p=0.7482, exp=0.75, p-val=0.19548
Variant: x=12189, obs=24425, p=0.4990, exp=0.5, p-val=0.76362
98000: 304.4058
{'Sample A/B test': {'Control': 12372, '(Excluded)': 73327, 'Variant': 12301}}
Control: x=12372, obs=24673, p=0.5014, exp=0.5, p-val=0.65126
(Excluded): x=73327, obs=98000, p=0.7482, exp=0.75, p-val=0.20293
Variant: x=12301, obs=24673, p=0.4986, exp=0.5, p-val=0.65126
99000: 304.6246
{'Sample A/B test': {'Control': 12475, '(Excluded)': 74100, 'Variant': 12425}}
Control: x=12475, obs=24900, p=0.5010, exp=0.5, p-val=0.75135
(Excluded): x=74100, obs=99000, p=0.7485, exp=0.75, p-val=0.27188
Variant: x=12425, obs=24900, p=0.4990, exp=0.5, p-val=0.75135
```

where:
* 95000: 304.1694 shows the amount of splits/second that the HTTP requests are able to ingest (single core, i7 7700K)
* {'Sample A/B test': ...} shows the assigned users per test.
* The remaining rows perform the significance test for each split group. The last value (p-val) should almost never (read 2.5% of the cases) go under 0.025, and if it falls well under 0.0001 we could be facing a case of bias.

This test should be repeated for many experiment names, sample sizes, group splits and many other thinkable combinations. Actually it has been used during the first stage of depelopment in order to asses the correctness of the implementation.

The test is performed in two stages:

1. Test over the audience split. This affects the whole sample.
2. Split between groups for the users that passed the audience filter. In the case above it only affected 25% of the sample.

The second test is hierarchically dependent on the first, but both split procedures should be considered statistically independent tests (we could have an error in the audience split, but the group split could show correct).

### CLI example 001: 100,000 random splits

The script performs the CLI version of the HTTP example. The calculation only uses the core calculation algorithm but it does not even load the module.

### CLI example 002: Usage of urandom (/dev/random)

A follow-up of the previous example but using the os.urandom() function, which could be using /dev/random or similar implementations.

That example helps showing more cases where the same calculation and split process can be fed by many elements.

### CLI example 003: Double split feature to implement the audience filter

The example shows more applications of the split procedure in order to randomize features like the experiment audience percent. There are more strategies to use that split algorithm in more smart ways, like user randomized groups and similar cases.

### CLI example 004: Realistic unbalanced experiment split

Uses the same configuration as in the HTTP interface, with the main difference of sending the raw data. The groups have been set to 70%/10%/10%/10% in order to detect any imbalance that could arise from the random generator.

### CLI example 005: Realistic balanced experiment split with UUID users

Uses the same configuration as in the HTTP interface, with the main difference of sending the raw data. The groups have been set to equal sizes 25%.

## Further steps

Although this project has a very narrow goal on the basic implementation of a random splitter, There are three areas where I plan to expect improving that tool:

* Variety: Decouple the hashing algorithm in order to implement alternative methods.
* Evaluation: Introduce a test suite for algorithms evaluation. Nothing necessarily comprehensive, but could be
* Speed: Find ways to perform such splits faster, by either moving some parts of the process to python, numpy or both.

Finally, please note that this project does not aim to replace any other similar opensource tool available in the market, but it's my hope that it can serve as a basecamp for quick findings and understanding of such pseudorandom generation strategies.
