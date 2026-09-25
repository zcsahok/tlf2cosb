setup() {
    bats_load_library bats-support
    bats_load_library bats-assert

    # get the containing directory of this file
    # use $BATS_TEST_FILENAME instead of ${BASH_SOURCE[0]} or $0,
    # as those will point to the bats executable's location or the preprocessed file respectively
    DIR="$( cd "$( dirname "$BATS_TEST_FILENAME" )" >/dev/null 2>&1 && pwd )"
    # make executables in src/ visible to PATH
    PATH="$DIR/..:$PATH"
}

#
# NOTE: all tests use dry-run mode (-n) to prevent actual score submission
#

@test "Unknown contest" {
    run tlf2cosb.pyz -n -i $DIR/minimal.ini -l $DIR/my.log -c asdf
    assert_failure
    assert_output --partial 'ERROR - Contest "asdf" not found'
}

@test "Contest found, but no log file" {
    run tlf2cosb.pyz -n -i $DIR/minimal_10qrp.ini -l $DIR/no.log -c sac-cw
    assert_failure
    assert_output --partial 'Scandinavian Activity, CW'
    assert_output --partial 'ERROR - Unable to read log file:'
}

@test "MWC (one mult) - SOAB-LP" {
    run tlf2cosb.pyz -n -i $DIR/minimal.ini -l $DIR/my.log -c mwc
    assert_success
    assert_output --partial '<contest>OK1WC</contest>'
    assert_output --partial '<score>30</score>'
    assert_output --partial '<class power="LOW"'
    assert_output --partial ' assisted="ASSISTED" transmitter="ONE" ops="SINGLE-OP" '
    assert_output --partial ' bands="ALL" mode="CW"'
    assert_output --partial '<point band="total" mode="ALL">6</point>'
    assert_output --partial '<mult band="total" mode="ALL" type="wpxprefix">5</mult>'
    assert_output --partial 'WARNING - Submission disabled; exiting.'
}

@test "TTC (no mults) - SO40-HP" {
    run tlf2cosb.pyz -n -i $DIR/minimal_40hp.ini -l $DIR/my.log -c ttc
    assert_success
    assert_output --partial '<contest>TTC-SPCWC</contest>'
    assert_output --partial '<score>6</score>'
    assert_output --partial '<class power="HIGH"'
    assert_output --partial ' bands="40M" mode="CW"'
    assert_output --partial '<point band="total" mode="ALL">6</point>'
    refute_output --partial '<mult'
}

@test "10-10 Winter SSB (no mults) - SO10-QRP" {
    run tlf2cosb.pyz -n -i $DIR/minimal_10qrp.ini -l $DIR/my_10ssb.log -c 'winter ssb'
    assert_success
    assert_output --partial '<contest>10-10</contest>'
    assert_output --partial '<score>12</score>'
    assert_output --partial '<class power="QRP"'
    assert_output --partial ' assisted="NON-ASSISTED" transmitter="ONE" ops="SINGLE-OP" '
    assert_output --partial ' bands="10M" mode="SSB"'
    assert_output --partial ' overlay="WIRE-ONLY"'
    assert_output --partial '<qso band="10" mode="SSB">6</qso>'
    assert_output --partial '<point band="10" mode="SSB">12</point>'
    assert_output --partial '<qso band="total" mode="ALL">6</qso>'
    assert_output --partial '<point band="total" mode="ALL">12</point>'
    refute_output --partial '<mult'
    refute_output --partial 'CW'
}

@test "CQ WW RTTY (two mults, auto rtty switch, no options)" {
    run tlf2cosb.pyz -n -i $DIR/cq_ww_rtty.ini
    assert_success
    assert_output --partial '<contest>CQ-WW-RTTY</contest>'
    assert_output --partial '<score>132</score>'
    assert_output --partial '<class power="LOW"'
    assert_output --partial ' assisted="ASSISTED" transmitter="ONE" ops="SINGLE-OP" '
    assert_output --partial ' bands="ALL" mode="RTTY"'
    assert_output --partial ' overlay="N/A"'
    assert_output --partial '<qso band="80" mode="RTTY">5</qso>'
    assert_output --partial '<point band="80" mode="RTTY">9</point>'
    assert_output --partial '<mult band="80" mode="RTTY" type="country">5</mult>'
    assert_output --partial '<mult band="80" mode="RTTY" type="zone">3</mult>'
    assert_output --partial '<qso band="total" mode="ALL">6</qso>'
    assert_output --partial '<point band="total" mode="ALL">12</point>'
    assert_output --partial '<mult band="total" mode="ALL" type="country">7</mult>'
    assert_output --partial '<mult band="total" mode="ALL" type="zone">4</mult>'
    refute_output --partial 'CW'
    refute_output --partial 'SSB'
}
