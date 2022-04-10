*** Settings ***
Documentation    Suite description
#Library SeleniumLibrary
Library     C:/Assignment/oppenheimerAutomation/Lib/Tax.py
Library     RequestsLibrary
Library     Collections


*** Variables ***
${base_url}      http://localhost:8080
${file}     C:\Assignment\oppenheimer-project-dev\Input.csv

*** Test Cases ***

Test Application status
    [Tags]  appstatus
    create session  mysession   ${base_url}
    ${response}=    get request     mysession   /
    log to console  ${response.status_code}
    #Validation
    ${status_code}=     convert to string   ${response.status_code}
    should be equal     ${status_code}    200

User Story 1 Test Insert single working class
    [Tags]  single
    create session  mysession   ${base_url}
    ${body}=    create dictionary   birthday=15121999  gender=F  name=John  natid=N09676  salary=6000  tax=125.00
    ${header}=   create dictionary   content-type=application/json
    ${response}=    post request     mysession   /calculator/insert     data=${body}    headers=${header}
    log to console  ${response.status_code}
    log to console  ${response.content}

    #Validation
    ${status_code}=     convert to string   ${response.status_code}
    should be equal     ${status_code}    202


User Story 2 Test Insert multiple working class
    [Tags]  multi
    create session  mysession   ${base_url}
    ${D1}=  create dictionary   birthday=15121999  gender=F  name=John  natid=N2676  salary=2000  tax=125.00
    ${D2}=  create dictionary   birthday=15121999  gender=M  name=John  natid=N3676  salary=3000  tax=125.00
    ${D3}=  create dictionary   birthday=15121999  gender=F  name=John  natid=N4676  salary=4000  tax=125.00
    @{body}=    create list     ${D1}   ${D2}   ${D3}
    ${header}=   create dictionary   content-type=application/json
    ${response}=    post request     mysession   /calculator/insertMultiple     data=@{body}    headers=${header}
    log to console  ${response.status_code}
    log to console  ${response.content}

    #Validation
    ${status_code}=     convert to string   ${response.status_code}
    should be equal     ${status_code}    202


User Story 4 Test Tax relief Get
    [Tags]  taxrelief
    create session  mysession   ${base_url}
    ${response}=    get request     mysession   /calculator/taxRelief
    log to console  ${response.status_code}
    log to console  ${response.content}

    #Validation
    ${status_code}=     convert to string   ${response.status_code}
    should be equal     ${status_code}    200
    ${natidformat}=   natid validation    ${response.content}
    should be equal     ${natidformat}    True

User Story 4 Test complete flow
    [Tags]  taxcalc
    create session  mysession   ${base_url}
    ${body}=    create dictionary   birthday=15121912  gender=M  name=John  natid=N91676  salary=300  tax=270.50
    ${header}=   create dictionary   content-type=application/json
    ${response}=    post request     mysession   /calculator/insert     data=${body}    headers=${header}
    ${response}=    get request     mysession   /calculator/taxRelief
    ${taxcalculation}=   calculate tax relief   ${body}     ${response.content}

    #Validation
    ${status_code}=     convert to string   ${response.status_code}
    should be equal     ${status_code}    200

*** Keywords ***
