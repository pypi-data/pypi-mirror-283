
# Queries templates for climdex

This folder contains the templates queries to online datacubes
that were selected as building blocks for the climate service.


## Categories

The queries are grouped into different categories, depending on
the output that is sought for, and the type of analysis involved:

 - *spatial_maps/*
   Queries in this category (identifier = `map`) produce 2D maps
   either on the full extent of the input, or a part of it;
   single time slices or algebraic combinations of
   one or more (aggregations of) time slices;

 - *trends/*
   Queries in this category (identifier = `trn`) yield 1D trends
   over a point or an area, above all trends of a variable, or
   an algebraic combinations of one or more variables across a dimension;

 - *uncertainty/*
   Queries in this category (identifier = `unc`) analyze the uncertainty
   and coherence of climate ensembles by inspecting the inter-models and
   intra-ensemble behaviours.

The extension suffix of each query file identifies a different
server type target, namely ".wcps" for rasdaman OGC WCPS server,
and ".json" for openEO processing graphs.

Each query can also have a correspondent `.md` file containing a
(markdown) description of the purpose and auxiliary information.


## Naming convention

The naming convetion of each query file is as follows
(a separate convention is described for each category for more clarity):

```
cat = map -> map_type[_igeom][_eaggr][_maggr][_taggr]_ifreq.ext
cat = trn -> trn_type[_igeom][_eaggr][_maggr][_taggr][_saggr]_ifreq.ext
cat = unc -> unc_type[_igeom][_saggr][_eaggr][_taggr]_ifreq.ext
```

where:

 - `cat` is the identifier of the category, as presented above;

 - `type` is a free label describing succintly the purpose of the query;

 - `igeom` is the input spatial geometry used to filter the input,
    it can be either `pnt` for point, `env` for envelope (bounding box),
    or `pol` for polygon; when not mentioned, no spatial filtering
    is mentioned at all in the query, and its full extent will be considered;

 - `*aggr` are the aggregation types used to aggregate out different
    cube dimension, namely `s` for spatial dimnensions,
    `maggr` for models within en ensemble,
    `eaggr` for RCP emissions scenarios, and `taggr` for the time dimension;
    an aggregation can either be `avg`, `max`, `min`, `pXX` for the
    XX-th percentile, having `med` as shortcuts for `p50`
    (median) and `qX` (X = {1,2,3}) for the three quartiles.
    NOTE: the letter `s`, `m`, `e` and `t` shall be used as prefixes
    in order to identify the dimension the aggregation type refers to
    in the query filename.

 - `ifreq` is the time-step of the input target indices, either
    `m` (month) or `y` (year): queries of the same type take different forms
    depending on the temporal configuration of the target cubes;

 - `ext` is the file suffix identifying the target server type, as mentioned
    above (either OGC WCPS or openEO services)


### Examples

Here's a few examples of query template names:

 1. `map_timestep.y.json`
    Having no aggregations, in none of the non-spatial dimensions,
    this query is used to extrac a single spatial map, at a specific
    time instant, a given model in the ensamble, and a given emissions
    scenario, from an input climate index with yearly time-step,
    in an openEO server.

 1. `map_timestep_mavg_tmed.y.json`
    Query the spatial 2D visualization of the ensemble average
    (either on the whole available models, or a subset of it),
    of the pixel-by-pixel median value among a given time interval,
    for a specific emissions scenario (again, yearly index input,
    and openEO target server).

 1. `map_timestep_pol_mavg_tmed.y.json`
    The same as above, but clipped on an input polygon.

 1. `trn_time_sp95_mmax.m.wcps`
    Query the trend over time (either the whole time extent available,
    or a part of it) of the 95th percentile of each spatial map of the
    maximums among the avaiable models in the ensemble, for a given
    emissions scenario (monthly input index, OGC WCPS target server).

 1. `trn_scenario_delta_smed_mmed.y.wcps`
    This query suggests that it will the the "delta" (i.e. the difference)
    among to emissions scenarios of the averaged (statistical median) values
    across both models of the ensemble and pixels over the region
    (yearly input index, OGC WCPS target server).

 1. `trn_scenario_delta_pnt_mmed.y.wcps`
    The same as in the previous example, but the trend is taken on a single
    spatial point.

 1. `unc_spread_tavg.y.json`
    This query suggests that the "spread" (max-min) of an enseamle is explored
    pixel-by-pixel and by averaging the values over a certain time interval,
    for a specific emissions scenario (yearly input index, openEO target server);

 1. `unc_count_pos_delta_env_tavg.m.json`
    This query suggests that it will detect the number of those model
    within an ensemble whose difference (delta) values between the averages
    over two time periods will be positive (not negative), over a reduced
    spatial subset (env = bounding-box) of the whole extent
    (monthly input index, openEO target server).



