# Prompt for Claude

Analyse every file in this folder as an evidence reviewer helping a Malaysian township competition team validate a real problem. Do not propose prototypes yet.

## Main question

Which pedestrian/walkability problem, if solved in one Malaysian township, is supported by the clearest evidence of repeated pain and is likely to benefit the largest number of people?

## Required method

1. Read `README.md` first, then inspect every numbered source.
2. Build an evidence matrix with: source number, geography, year, sample/method, population, reported problem, quantitative result, evidence strength, bias/limitation, and what the source can and cannot prove.
3. Separate:
   - national scale/severity evidence;
   - local causal or diagnostic evidence;
   - policy/design guidance;
   - qualitative social-media signals.
4. Code recurring barriers such as route discontinuity, unsafe crossings/traffic, obstruction and maintenance, shade/heat/rain, lighting and personal security, universal accessibility, distance/land use, first/last-mile connectivity, enforcement, and social norms.
5. Do not count Reddit comments as survey responses, infer population percentages from them, or use them to validate monetary claims.
6. Do not combine percentages across studies with different populations or methods.
7. Identify contradictions and alternative explanations. In particular, test whether inactivity is caused by infrastructure, climate, distance, preferences, time, public-transport quality, or several interacting factors.
8. Distinguish a broad national problem from a problem that can be acted on in one township.

## Deliverables

Provide:

1. A one-paragraph conclusion naming the best-supported problem.
2. A ranked list of the top five problem statements, each written as: **[user] struggles to [job] because [barrier], causing [measurable harm].**
3. The evidence matrix.
4. A theme-convergence table showing which independent sources support each barrier.
5. A confidence rating (high/medium/low) for every important claim.
6. The five most important evidence gaps.
7. The smallest, fastest validation plan for one selected township, using existing datasets first and no more than five short interviews only where secondary evidence cannot answer the question.
8. A final “claims safe to use in competition slides” section with precise source references and a separate “claims not yet safe to use” section.

Be sceptical. Prefer primary and official sources, preserve methodological caveats, and say when the evidence does not justify a conclusion.
