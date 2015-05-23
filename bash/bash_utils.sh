#!/bin/bash

##########################################################
# Common and useful bash operations.
# 1. String manipulations.
# 2. patch manipulations.
##########################################################

##########################################################
# Note on functions:
# ------------------
# There is no way good way to return a value from a bash
# function. One way to do that is to echo on stdout.
# But be careful not to echo other values on stdout from
# the function.
##########################################################

function get_string_len () {
    local str=$1
    echo "${#str}"
}

function get_substr_from_index () {
    local str=$1
    local idx=$2

    if [[ -z $3 ]]; then
        substrlen=${#str}
    else
        substrlen=$3
    fi

    echo ${str:$idx:$substrlen}
}

# Match two strings. One is a substring of another.
# true: match found, false: otherwise
function check_substring ()
{
    local str=$1
    local substr=$2

    if [[ ${str/$substr} != ${str} ]]; then
        echo true 
    else
        echo false 
    fi
}

# Match and remove $2 (substring) in $1 (string)
function substring_del_front () {
    local str=$1
    local substr=$2

    echo ${str#*$substr}
}

# Match and remove $2 (substring) in $1 (string)
# from the end.
function substring_del_end () {
    local str=$1
    local substr=$2

    echo ${str%$substr*}
}

# Match and replace $2 (substring) in $1 (str) with
# $3 (replace)
function replace_any_one () {
    local str=$1
    local substr=$2
    local replace=$3

    echo ${str/$substr/$replace}
}

function replace_any_all ()
{
    local str=$1
    local substr=$2
    local replace=$3

    echo ${str//$substr/$replace}
}

function replace_begin ()
{
    local str1=$1
    local substr=$2
    local replace=$3

    echo ${str/#$substr/$replace}
}

function split_string () {
    local str1=$1
    local delim=$2

    if [[ -z $delim ]]; then
        # Set default to =
        delim="="
    fi

    echo "String: ${str1}"
    echo "String: ${str1##*$delim}"
}

function test_operation () {
    local func_name=$1
    eval $func_name "test" 
}

# Function to test taking variable number of
# arguments as strings and saving them into
# an array of user arguments.
function test_variableargs ()
{
    args=$@
    #echo "arg[0]: ${args[0]}"
    #echo "arg[*]: ${args[*]}"
    #echo "arg[2]: ${args[2]}, ${args[1]}"

    #echo "All arguments: ${args[@]}"

    declare -a argarr
    idx=-1
    for arg in ${args[@]}; do
        echo "arg:: ${arg}"
        if [[ ${arg/"arg:"} != ${arg} ]]; then
            # Start a new argument.
            arg=${arg/"arg:"/}
            idx=$((idx+1))
            argarr[idx]=${arg}
        else
            echo "Append $arg to existing $idx"
            argarr[idx]="${argarr[idx]} ${arg}"
            echo "appended arg: ${argarr[idx]}"
        fi
    done
    IFS=""
    for arg in ${argarr[@]}; do
        echo "argument: $arg"
    done
}
