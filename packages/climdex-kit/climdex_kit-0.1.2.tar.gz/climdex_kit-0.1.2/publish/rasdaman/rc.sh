#!/bin/bash

#####################################################################
# Commands for i) generating rasdaman JSON ingredients files for each
# climate index ensembles found in a given input directory, and ii)
# import them in rasdaman as OGC WCS Coverages.
#
# The climate indices are published as 5D coverages:
#
#     - time
#     - 2D space
#     - models of ensamble
#     - RCP scenario
#
# input:
#    - ./etc/ras_conn        : rasdaman connections parameters
#    - ./etc/models_lut.json : Look-Up Table to index climate models of the ensambles
#    - ./INDEX_19712100_tnst_1x1km_${freq}_cordexadj_qdm.json.in :
#         template ingredients file, one per each $freq = "frequency" NetCDF attribute
#         of the input time-series.
#    - ./*.json              : other static ingredient file that will be copied to the
#                              ingredients/ folder and imported with no prior processing
#
# output:
#    - JSON ingredients files under the ./ingredients/ folder
#    - climate indices coverages uploaded to rasdaman
#
# environment vars to override default behaviour:
#    - IDIR  :  root input folder with indices NetCDFs
#               following the $IDIR/$index/$scenario/$model.nc structure.
#               Default: "/mnt/CEPH_PROJECTS/FACT_CLIMAX/CORDEX-Adjust/INDICES"
#
# @author: pcampalani
#####################################################################

# FIXME: rcp45/rcp85 fixed input scenarios in INDEX json templates.

ME="$( basename $0 )"
alias log='echo ${bold}[$ME]${normal} '
alias logn='echo -n ${bold}[$ME]${normal} '
shopt -s expand_aliases

# store script dir
PWD="$( pwd )"
SOURCE="${BASH_SOURCE[0]}"
SCRIPT_DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
#cd -P "$PWD" # back to shp folder

# exit codes
CODE_OK=0
CODE_WRONG_USAGE=1
CODE_RMAN_CONN_MISSING=2
CODE_MLUT_MISSING=3
CODE_CDO_NOT_INSTALLED=4
CODE_NDO_NOT_INSTALLED=5
CODE_WCST_IMP_NOT_INSTALLED=6
CODE_IDIR_ILLEGAL=7
CODE_SIGINT=99

# env
CLIMAX="/mnt/CEPH_PROJECTS/FACT_CLIMAX"
IDIR="${IDIR:-$CLIMAX/CORDEX-Adjust/INDICES}"
ODIR="./ingredients"

# connection files
RASDAMAN_CONN="./etc/ras_conn"
MODELS_LUT_JSON="./etc/models_lut.json"

#
# deps checks
#
if [ ! -f "$SCRIPT_DIR/$RASDAMAN_CONN" ]; then
    echo "\"$RASDAMAN_CONN\" not found."
    exit $CODE_RMAN_CONN_MISSING
fi
. "$SCRIPT_DIR/$RASDAMAN_CONN"

if [ ! -f "$SCRIPT_DIR/$MODELS_LUT_JSON" ]; then
    echo "\"$MODELS_LUT_JSON\" not found."
    exit $CODE_MLUT_MISSING
fi

if [ ! -d "$IDIR" ]
then
    echo "Input root directory does not exist: \"$IDIR\""
    exit $CODE_IDIR_ILLEGAL
fi

CDO="$( which cdo )"
if [ $? -ne 0 ]
then
    echo "CDO toolkit not found: which cdo. Please install it and retry."
    exit $CODE_CDO_NOT_INSTALLED
fi

NCAP2="$( which ncap2 )"
if [ $? -ne 0 ]
then
    echo "NCO toolkit not found: which ncap2. Please install it and retry."
    exit $CODE_NCO_NOT_INSTALLED
fi

WCST_IMPORT="$( which wcst_import.sh )"
if [ $? -ne 0 ]
then
    echo "wcst_import.sh not found. Please install it and retry."
    exit $CODE_WCST_IMP_NOT_INSTALLED
fi

#
# templates
#
declare -A templates
yearly="year"
monthly="mon"

for freq in $yearly $monthly
do
    templates[$freq]="INDEX_19712100_tnst_1x1km_${freq}_cordexadj_qdm.json.in"
done

# CTRL-C
trap printout SIGINT
printout() {
    log
    log "Interrupt. Bye.."
    exit $CODE_SIGINT
}

#
# start:
#
log
log "rasdaman ingredients templates:"
for key in ${!templates[@]}; do
    log "   + ${key} -> ${templates[${key}]}"
done

log "Indices directory (\$IDIR)  : \"$IDIR\""
log "Output directory           : \"$ODIR\""
log "rasdaman endpoint          : \"$RMAN_OWS_URL\""
log "wcst_import used           : \"$WCST_IMPORT\""

if [ ! -d "$ODIR" ]
then
    mkdir "$ODIR"
fi

# are there existing ingredients already?
n_jsons=$( find "$ODIR" -name "*.json" | wc -l )

#
# Create JSON ingredients from templates
#
log && logn
if [[ $n_jsons -eq 0 || "$(read -e -p " Re-create index ingredients files and overwrite existing $ODIR/*.json files? [y/N]> "; echo $REPLY)" == [Yy]* ]]
then
    for index_dir in $( find "$IDIR" -mindepth 1 -maxdepth 1 -type d -not -name '.*' | sort )
    do
        index="$( basename "$index_dir" )"
        logn " :: $index "

        test_nc="$( find "$index_dir" -mindepth 2 -maxdepth 2 -type f -name "${index}*\.nc" | head -n 1 )"
        if [ ! "$test_nc" ]
        then
            echo "[!] No \"${index}*.nc\" NetCDF found in folder. Skipping..."
        fi

        freq_attr=$( $CDO --silent showattribute,frequency "$test_nc" 2>&1 | tail -n 1 | sed "s/^.*frequency = \"\(.*\)\".*$/\1/g" )
        if [ ! "$freq_attr" ]
        then
            echo "[!] \"frequency\" attribute not found in test NetCDF \"$test_nc\". Skipping index."
            continue
            # folders=( index1 index2 ... )
            # for folder in ${folders[@]}; do
            #   for innc in $( find "$CLIMAX/CORDEX-Adjust/INDICES/$folder" -name "*.nc" ); do
            #      cdo --history setattribute,frequency='year' "$innc" out.nc; mv out.nc $innc
            #   done
            # done
        elif [ ! "${templates[$freq_attr]}" ]
        then
            echo "[!] No template ingredients found for input frequency \"$freq_attr\". Available: {${!templates[@]}}"
            continue
        else
            template="${templates[$freq_attr]}"
            ingr_file="$( echo "$template" | sed -e "s/INDEX/$index/g" )"
            cov_id="$( basename "${ingr_file%%.*}" )"

            # build paths, one per each scenario # TODO
            # printf -v paths_csv '%s,\n' "${paths[@]}"
            # paths=$( echo "${path_csv%,}" )

            echo -n " -> $ingr_file... "
            cat "$template" |
                sed "s/{{ows_url}}/$( echo $RMAN_OWS_URL | sed 's;/;\\/;g' )/g" | # escape backslashes in path
                sed "s/{{tmp_dir}}/$( echo $RMAN_TMP_DIR | sed 's;/;\\/;g' )/g" | #
                sed "s/{{def_dir}}/$( echo $RMAN_CRS_RES | sed 's;/;\\/;g' )/g" | #
                sed "s/{{models_lut_file}}/$( echo "$MODELS_LUT_JSON" | sed 's;/;\\/;g' )/g" | # [!] python import wrt to wcst_import caller dir
                sed "s/{{coverage_id}}/$cov_id/g"              |
                sed "s/{{index}}/$index/g"                     > "$ODIR/${ingr_file%.*}"
            echo "Ok."
        fi
    done
fi

#
# harmonize models among scenarios to avoid insertions in the middle
# along the model dimension M
#
log && logn
if [[ "$(read -e -p " Harmonize ensembles between scenarios in \"$IDIR\" files with empty time-series? [y/N]> "; echo $REPLY)" == [Yy]* ]]
then
    for ingr_file in $( find "$ODIR" -maxdepth 1 -type f -name '*.json' | sort )
    do
        log " :: $ingr_file "

        declare -A ensembles

        # discover models of ensemble for each scenario
        for path in $( cat $ingr_file | sed -n "s,\"\($IDIR.*\)\".*,\1,p" )
        do
            scenario=$( basename $( dirname "$path" ) )
            index=$( basename $( dirname $( dirname "$path" ) ) )
            model=$( basename $path | sed -n "s/${index}_\(.*\)_${scenario}.nc/\1/p" )

            ensembles[$scenario]+=" $model"
        done

        # models lists to file
        declare -A ens_files
        for scenario in ${!ensembles[@]}
        do
            file="${scenario}.ens"
            ens_files[$scenario]="$file"
            echo ${ensembles[$scenario]} | tr " " "\n" | sort | uniq > "$file"
        done

        # merge all models to uniqe complete list
        all_models_file="all_models.ens"
        cat ${ens_files[@]} | sort | uniq > "$all_models_file"

        # find missing models for each scenario and create empty placeholder NetCDFs
        for scenario in ${!ens_files[@]}
        do
            test_nc="$( find "${IDIR}/${index}/${scenario}" -maxdepth 1 -type f -name "${index}*\.nc" | head -n 1 )"
            if [ ! "$test_nc" ]
            then
                echo "[!] No \"${index}*.nc\" NetCDF found in folder. Skipping..."
                break
            fi

            for model in $( grep -Fxvf "${ens_files[$scenario]}" "$all_models_file" )
            do
                logn "     Missing ${scenario}::${model}... "
                ofile="${IDIR}/${index}/${scenario}/${index}_${model}_${scenario}.nc"
                #"$CDO" --silent --history -expr,"${index}=missval(${index})" "$test_nc" "$ofile" -> DROPS GLOBAL ATTRIBUTES
                $NCAP2 --history -s "${index}=${index}*0 + ${index}.get_miss()" "$test_nc" "$ofile"
                chmod 664 "$ofile"
                echo  "Done."
            done
        done

        # cleanup
        rm -v ${ens_files[@]} "$all_models_file" >/dev/null
        unset ensembles ens_files
    done
fi

#
# other auxiliary ingredient templates file to be imported?
#
# NOTE-1: always template, as the rasdaman endpoint must ne coherent with this script's config
# NOTE-2: we must exclude the index templates from this count
# NOTE-3: the coverage id is the basename of the json file itself
#

n_jsons=$( find "$PWD" -maxdepth 1 -type f -name "*.json.in" | wc -l )

if [ $n_jsons -gt ${#templates[@]} ]
then
    log && logn
    if [[ "$(read -e -p " Import static *.json.in files? [y/N]> "; echo $REPLY)" == [Yy]* ]]
    then
        for index_dir in $( find "$PWD" -maxdepth 1 -type f -name '*.json.in' | sort )
        do
            json="$( basename "$index_dir" )"
            if [[ ! " ${templates[@]} " =~ " $json " ]]
            then
                logn " :: $json... "
                cov_id="$( basename "${json%%.*}" )"
                cat "$json" |
                    sed "s/{{ows_url}}/$( echo $RMAN_OWS_URL | sed 's;/;\\/;g' )/g" | # escape backslashes in path
                    sed "s/{{tmp_dir}}/$( echo $RMAN_TMP_DIR | sed 's;/;\\/;g' )/g" | #
                    sed "s/{{def_dir}}/$( echo $RMAN_CRS_RES | sed 's;/;\\/;g' )/g" | #
                    sed "s/{{coverage_id}}/$cov_id/g"        > "$ODIR/${json%.*}"

                # search for the file that has been created right now:
                if [ $(find "$ODIR" -mmin -1 -type f -name "${json%.*}" | wc -l) -eq 0 ]
                then
                    echo "[!] ERROR skipping"
                    continue
                else
                    echo "Ok."
                fi
            fi
        done
    fi
fi

#
# WCS-T import
#
log && logn
if [[ "$(read -e -p " Do you want to publish all ingredients in \"$ODIR\" to rasdaman <${RMAN_OWS_URL}>? [y/N]> "; echo $REPLY)" == [Yy]* ]]
then
    for ingr_file in $( find "$ODIR" -mindepth 1 -maxdepth 1 -type f -name '*.json' | sort )
    do
        mock=$( cat "$ingr_file" | sed -n 's/^.*"mock": \([a-z]\+\).*$/\1/p' )
        mock=$( [[ $mock = 'true' ]] && echo -n "[mock] " )

        logn " :: $mock$( basename $ingr_file )... "

        $WCST_IMPORT "$ingr_file" >/dev/null 2>&1
        if [ $? -ne 0 ]
        then
            echo "[!] ERROR skipping"
            continue
        else
            echo "Ok."
        fi
    done
fi

log "Bye.."
exit $CODE_OK
