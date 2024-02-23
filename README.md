# PyMTDEvaluator2
Updated version of PyMTDEvaluator with support for Multi-Criteria Decision Making Methods



**For results extraction:**

	docker exec <container-ID> ./zipResults.sh
	docker cp <container-ID>:/Results.zip .

We recommend to start a new container for each round of evaluations. 

**Errors while using MCDM methods:**

In general, errors occur when the parameters present anomalies (e.g., short time for attack success and late VM migrations, etc). Some examples are below. In case you find errors like: "raise ValueError(f"The data {values} doesn't look like a ranking")", please check your parameters. 

1) Zero value for any of the criteria

	At this version of PyMTDEvaluator, we need to have at least 1% of weight for the each of the criteria. Zero values cause errors in the data transformation for the evaluation. 

2) Errors in shorter evaluations without MTD action.

	Evaluation time shorter than the movement trigger leads to cost=0. Therefore, the MCDM method will produce errors in the evaluation. 

