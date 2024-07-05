###############################################################################
# (c) Copyright 2019 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
"""Unit tests for Workflow Module ErrorLogging."""

import json
import pytest
import os
from pathlib import Path

from DIRAC import S_OK
from LHCbDIRAC.Workflow.Modules.ErrorLogging import ErrorLogging
from LHCbDIRAC.Workflow.Modules.test.mock_Commons import (
    prod_id,
    prod_job_id,
    wms_job_id,
    workflowStatus,
    step_id,
    step_number,
    step_commons,
    wf_commons,
)


# Helper Functions
@pytest.fixture
def errorlog(mocker):
    """Fixture for ErrorLogging module."""
    mocker.patch("LHCbDIRAC.Workflow.Modules.ModuleBase.RequestValidator")
    mocker.patch("LHCbDIRAC.Workflow.Modules.ErrorLogging.ErrorLogging._resolveInputVariables")

    errorlog = ErrorLogging()

    yield errorlog

    # Teardown
    errorLogName = f"{prod_id}_Errors_{errorlog.applicationName}.json"
    Path(errorLogName).unlink(missing_ok=True)


# Test Scenarios
def test_errorLogging_gauss_noError_success(errorlog):
    """Test successful execution of ErrorLogging module for Gauss application: there is no error."""
    # Mock the ErrorLogging module for Gauss application
    errorlog.applicationName = "Gauss"
    errorlog.applicationVersion = "v49r10"
    errorlog.applicationLog = "gauss.log"
    errorlog.errorLogNamejson = f"{prod_id}_Errors_{errorlog.applicationName}.json"

    # Create a mock log file
    logContent = "Sample Gauss log content without errors."
    with open(errorlog.applicationLog, "w") as logFile:
        logFile.write(logContent)

    assert errorlog.execute(
        production_id=prod_id,
        prod_job_id=prod_job_id,
        wms_job_id=wms_job_id,
        workflowStatus=workflowStatus,
        wf_commons=wf_commons[0],
        step_commons=step_commons[0],
        step_number=step_number,
        step_id=step_id,
    )["OK"]

    # Check if the error log file is created
    assert Path(errorlog.errorLogNamejson).exists(), "Error log JSON file not created."

    with open(errorlog.errorLogNamejson) as errorLog:
        errorContent = json.load(errorLog)

    assert errorContent["JobID"] == prod_job_id, "JobID not found in error log JSON file."
    assert errorContent["ProductionID"] == prod_id, "ProductionID not found in error log JSON file."
    assert errorContent["wmsID"] == wms_job_id, "wmsID not found in error log JSON file."
    assert errorContent["Application"] == errorlog.applicationName, "Application not found in error log JSON file."
    assert (
        errorContent["ApplicationVersion"] == errorlog.applicationVersion
    ), "ApplicationVersion not found in error log JSON file."
    assert errorContent["timestamp"] > 0, "timestamp not found in error log JSON file."

    # Clean up
    Path(errorlog.applicationLog).unlink(missing_ok=True)


def test_errorLogging_gauss_identicalg4Exceptions_success(errorlog):
    """Test successful execution of ErrorLogging module for Gauss application: there is 2 identical G4Exception."""
    # Mock the ErrorLogging module for Gauss application
    errorlog.applicationName = "Gauss"
    errorlog.applicationVersion = "v49r10"
    errorlog.applicationLog = "gauss.log"
    errorlog.errorLogNamejson = f"{prod_id}_Errors_{errorlog.applicationName}.json"

    # Create a mock log file
    logContent = """
    -------- WWWW ------- G4Exception-START -------- WWWW -------
    *** G4Exception : FTFP_BERT
      issued by : G4FTFPPionBuilder::Build()
    In G4FTFPPionBuilder::Build() pi+ Inelastic cross section is not available
    for 5.000000 TeV/c pi+.
    *** This is just a warning message. ***
    -------- WWWW -------- G4Exception-END --------- WWWW -------
    ...
    -------- WWWW ------- G4Exception-START -------- WWWW -------
    *** G4Exception : FTFP_BERT
      issued by : G4FTFPPionBuilder::Build()
    In G4FTFPPionBuilder::Build() pi+ Inelastic cross section is not available
    for 5.000000 TeV/c pi+.
    *** This is just a warning message. ***
    -------- WWWW -------- G4Exception-END --------- WWWW -------
    """
    with open(errorlog.applicationLog, "w") as logFile:
        logFile.write(logContent)

    assert errorlog.execute(
        production_id=prod_id,
        prod_job_id=prod_job_id,
        wms_job_id=wms_job_id,
        workflowStatus=workflowStatus,
        wf_commons=wf_commons[0],
        step_commons=step_commons[0],
        step_number=step_number,
        step_id=step_id,
    )["OK"]

    # Check if the error log file is created
    assert Path(errorlog.errorLogNamejson).exists(), "Error log JSON file not created."

    with open(errorlog.errorLogNamejson) as errorLog:
        errorContent = json.load(errorLog)

    assert errorContent["JobID"] == prod_job_id, "JobID not found in error log JSON file."
    assert errorContent["ProductionID"] == prod_id, "ProductionID not found in error log JSON file."
    assert errorContent["wmsID"] == wms_job_id, "wmsID not found in error log JSON file."
    assert errorContent["Application"] == errorlog.applicationName, "Application not found in error log JSON file."
    assert (
        errorContent["ApplicationVersion"] == errorlog.applicationVersion
    ), "ApplicationVersion not found in error log JSON file."
    assert errorContent["timestamp"] > 0, "timestamp not found in error log JSON file."

    # Make sure there is a single key starting with G4Exception
    # Get the key starting with G4Exception and check its value: should be 2
    assert len(errorContent.keys()) == 7, "Error log JSON file does not contain G4Exceptions."
    g4ExceptionKey = [key for key in errorContent.keys() if key.startswith("G4Exception : FTFP_BERT")][0]
    assert errorContent[g4ExceptionKey] == 2, "G4Exception count not found in error log JSON file."

    # Clean up
    Path(errorlog.applicationLog).unlink(missing_ok=True)


def test_errorLogging_gauss_differentg4Exceptions_success(errorlog):
    """Test successful execution of ErrorLogging module for Gauss application: there is 2 different G4Exception."""
    # Mock the ErrorLogging module for Gauss application
    errorlog.applicationName = "Gauss"
    errorlog.applicationVersion = "v49r10"
    errorlog.applicationLog = "gauss.log"
    errorlog.errorLogNamejson = f"{prod_id}_Errors_{errorlog.applicationName}.json"

    # Create a mock log file
    logContent = """
    -------- WWWW ------- G4Exception-START -------- WWWW -------
    *** G4Exception : FTFP_BERT
      issued by : G4FTFPPionBuilder::Build()
    In G4FTFPPionBuilder::Build() pi+ Inelastic cross section is not available
    for 5.000000 TeV/c pi+.
    *** This is just a warning message. ***
    -------- WWWW -------- G4Exception-END --------- WWWW -------
    ...
    -------- WWWW ------- G4Exception-START -------- WWWW -------
    *** G4Exception : PART102
        issued by : G4ParticleDefintion::G4ParticleDefintion
    Strange PDGEncoding
    *** This is just a warning message. ***
    -------- WWWW -------- G4Exception-END --------- WWWW -------
    """
    with open(errorlog.applicationLog, "w") as logFile:
        logFile.write(logContent)

    assert errorlog.execute(
        production_id=prod_id,
        prod_job_id=prod_job_id,
        wms_job_id=wms_job_id,
        workflowStatus=workflowStatus,
        wf_commons=wf_commons[0],
        step_commons=step_commons[0],
        step_number=step_number,
        step_id=step_id,
    )["OK"]

    # Check if the error log file is created
    assert Path(errorlog.errorLogNamejson).exists(), "Error log JSON file not created."

    with open(errorlog.errorLogNamejson) as errorLog:
        errorContent = json.load(errorLog)

    assert errorContent["JobID"] == prod_job_id, "JobID not found in error log JSON file."
    assert errorContent["ProductionID"] == prod_id, "ProductionID not found in error log JSON file."
    assert errorContent["wmsID"] == wms_job_id, "wmsID not found in error log JSON file."
    assert errorContent["Application"] == errorlog.applicationName, "Application not found in error log JSON file."
    assert (
        errorContent["ApplicationVersion"] == errorlog.applicationVersion
    ), "ApplicationVersion not found in error log JSON file."
    assert errorContent["timestamp"] > 0, "timestamp not found in error log JSON file."

    # Make sure there is a single key starting with G4Exception
    # Get the key starting with G4Exception and check its value: should be 1
    assert len(errorContent.keys()) == 8, "Error log JSON file does not contain G4Exceptions."
    g4ExceptionKey1 = [key for key in errorContent.keys() if key.startswith("G4Exception : FTFP_BERT")][0]
    g4ExceptionKey2 = [key for key in errorContent.keys() if key.startswith("G4Exception : PART102")][0]

    assert errorContent[g4ExceptionKey1] == 1, "G4Exception count not found in error log JSON file."
    assert errorContent[g4ExceptionKey2] == 1, "G4Exception count not found in error log JSON file."

    # Clean up
    Path(errorlog.applicationLog).unlink(missing_ok=True)


def test_errorLogging_gauss_malformedG4Exceptions_success(errorlog):
    """Test successful execution of ErrorLogging module for Gauss application: there is 2 malformed G4Exception."""
    # Mock the ErrorLogging module for Gauss application
    errorlog.applicationName = "Gauss"
    errorlog.applicationVersion = "v49r10"
    errorlog.applicationLog = "gauss.log"
    errorlog.errorLogNamejson = f"{prod_id}_Errors_{errorlog.applicationName}.json"

    # Create a mock log file
    logContent = """
        issued by : G4ParticleDefintion::G4ParticleDefintion
    Strange PDGEncoding
    *** This is just a warning message. ***
    -------- WWWW -------- G4Exception-END --------- WWWW -------
    -------- WWWW ------- G4Exception-START -------- WWWW -------
    *** G4Exception : PART102
        issued by : G4ParticleDefintion::G4ParticleDefintion
    Strange PDGEncoding
    *** This is just a warning message. ***
    """
    with open(errorlog.applicationLog, "w") as logFile:
        logFile.write(logContent)

    assert errorlog.execute(
        production_id=prod_id,
        prod_job_id=prod_job_id,
        wms_job_id=wms_job_id,
        workflowStatus=workflowStatus,
        wf_commons=wf_commons[0],
        step_commons=step_commons[0],
        step_number=step_number,
        step_id=step_id,
    )["OK"]

    # Check if the error log file is created
    assert Path(errorlog.errorLogNamejson).exists(), "Error log JSON file not created."

    with open(errorlog.errorLogNamejson) as errorLog:
        errorContent = json.load(errorLog)

    assert errorContent["JobID"] == prod_job_id, "JobID not found in error log JSON file."
    assert errorContent["ProductionID"] == prod_id, "ProductionID not found in error log JSON file."
    assert errorContent["wmsID"] == wms_job_id, "wmsID not found in error log JSON file."
    assert errorContent["Application"] == errorlog.applicationName, "Application not found in error log JSON file."
    assert (
        errorContent["ApplicationVersion"] == errorlog.applicationVersion
    ), "ApplicationVersion not found in error log JSON file."
    assert errorContent["timestamp"] > 0, "timestamp not found in error log JSON file."

    # Make sure there is a single key starting with G4Exception
    # Get the key starting with G4Exception and check its value: should be 2
    assert len(errorContent.keys()) == 7, "Error log JSON file does not contain G4Exceptions."
    g4ExceptionKey = [key for key in errorContent.keys() if key.startswith("G4Exception : PART102")][0]
    assert errorContent[g4ExceptionKey] == 1, "G4Exception count not found in error log JSON file."


def test_errorLogging_gauss_errors_success(errorlog):
    """Test successful execution of ErrorLogging module for Gauss application: there are some errors and warnings."""
    # Mock the ErrorLogging module for Gauss application
    errorlog.applicationName = "Gauss"
    errorlog.applicationVersion = "v49r10"
    errorlog.applicationLog = "gauss.log"
    errorlog.errorLogNamejson = f"{prod_id}_Errors_{errorlog.applicationName}.json"

    # Create a mock log file
    logContent = """
    2022-06-16 03:28:03 UTC EventLoopMgr      WARNING Unable to locate service "EventSelector"
    2022-06-16 03:28:03 UTC EventLoopMgr      WARNING No events will be processed from external input.
    2022-06-16 04:28:59 UTC /dd/Structure/L...  ERROR Gap not found!
    PYTHIA Error in Pythia::forceHadronLevel: hadronLevel failed; try again
    PYTHIA Warning in Pythia::check: energy-momentum not quite conserved
    WARNING: G4QCaptureAtRest is deprecated and will be removed in GEANT4 version 10.0.
    2022-06-16 04:28:59 UTC /dd/Structure/L...  ERROR Gap not found!
    """
    with open(errorlog.applicationLog, "w") as logFile:
        logFile.write(logContent)

    assert errorlog.execute(
        production_id=prod_id,
        prod_job_id=prod_job_id,
        wms_job_id=wms_job_id,
        workflowStatus=workflowStatus,
        wf_commons=wf_commons[0],
        step_commons=step_commons[0],
        step_number=step_number,
        step_id=step_id,
    )["OK"]

    # Check if the error log file is created
    assert Path(errorlog.errorLogNamejson).exists(), "Error log JSON file not created."

    with open(errorlog.errorLogNamejson) as errorLog:
        errorContent = json.load(errorLog)

    assert errorContent["JobID"] == prod_job_id, "JobID not found in error log JSON file."
    assert errorContent["ProductionID"] == prod_id, "ProductionID not found in error log JSON file."
    assert errorContent["wmsID"] == wms_job_id, "wmsID not found in error log JSON file."
    assert errorContent["Application"] == errorlog.applicationName, "Application not found in error log JSON file."
    assert (
        errorContent["ApplicationVersion"] == errorlog.applicationVersion
    ), "ApplicationVersion not found in error log JSON file."
    assert errorContent["timestamp"] > 0, "timestamp not found in error log JSON file."

    # Make sure there is a single key starting with G4Exception
    # Get the key starting with G4Exception and check its value: should be 1
    assert len(errorContent.keys()) == 7, "Error log JSON file should contain Errors."
    assert errorContent["ERROR Gap not found!"] == 2, "ERROR Gap not found! count not found in error log JSON file."

    # Clean up
    Path(errorlog.applicationLog).unlink(missing_ok=True)


def test_errorLogging_nonexistent_logfile(errorlog):
    """Test ErrorLogging when the log file does not exist."""
    # Mock the ErrorLogging module
    errorlog.applicationName = "Gauss"
    errorlog.applicationVersion = "v49r10"
    errorlog.applicationLog = "nonexistent.log"

    assert errorlog.execute(
        production_id=prod_id,
        prod_job_id=prod_job_id,
        wms_job_id=wms_job_id,
        workflowStatus=workflowStatus,
        wf_commons=wf_commons[0],
        step_commons=step_commons[0],
        step_number=step_number,
        step_id=step_id,
    )["OK"], "Execution should succeed even if log file is missing."

    # The nonexistence of the log file should not create an error log file
    errorLogName = f"{prod_id}_Errors_{errorlog.applicationName}.json"
    assert not Path(errorLogName).exists(), "Error log JSON file should not be created for nonexistent log."


def test_errorLogging_empty_logfile(errorlog):
    """Test ErrorLogging with an empty log file."""
    # Mock the ErrorLogging module
    errorlog.applicationName = "Gauss"
    errorlog.applicationVersion = "v49r10"
    errorlog.applicationLog = "empty.log"

    # Create an empty log file
    Path(errorlog.applicationLog).touch()

    assert errorlog.execute(
        production_id=prod_id,
        prod_job_id=prod_job_id,
        wms_job_id=wms_job_id,
        workflowStatus=workflowStatus,
        wf_commons=wf_commons[0],
        step_commons=step_commons[0],
        step_number=step_number,
        step_id=step_id,
    )["OK"], "Execution should succeed even with an empty log file."

    # The empty log file should not create an error log file
    errorLogName = f"{prod_id}_Errors_{errorlog.applicationName}.json"
    assert not Path(errorLogName).exists(), "Error log JSON file should not be created for an empty log."

    # Clean up
    os.remove(errorlog.applicationLog)


def test_errorLogging_non_gauss_boole_app(errorlog):
    """Test ErrorLogging when the application is neither Gauss nor Boole."""
    # Mock the ErrorLogging module for a non-Gauss/Boole application
    errorlog.applicationName = "NonGaussBooleApp"
    errorlog.applicationVersion = "v1.0"
    errorlog.applicationLog = "nonGaussBooleApp.log"

    assert errorlog.execute(
        production_id=prod_id,
        prod_job_id=prod_job_id,
        wms_job_id=wms_job_id,
        workflowStatus=workflowStatus,
        wf_commons=wf_commons[0],
        step_commons=step_commons[0],
        step_number=step_number,
        step_id=step_id,
    )["OK"], "Execution should succeed for non-Gauss/Boole applications."

    # Non-Gauss/Boole applications should not create an error log file
    errorLogName = f"{prod_id}_Errors_{errorlog.applicationName}.json"
    assert not Path(
        errorLogName
    ).exists(), "Error log JSON file should not be created for non-Gauss/Boole applications."
