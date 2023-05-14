function getServicesForSalon(){
    var inputTag = document.getElementById('businessNameInput');
    var jsonData = JSON.parse(inputTag.getAttribute('data-json'));
    var selectedText = document.getElementsByClassName('active')[0].textContent;
    for (salon of jsonData) {
        if (salon['text'] == selectedText) {
            break;
        }
    }
    var form = document.createElement('form');
    form.setAttribute('method', 'POST');
    form.setAttribute('style', 'display: none;');
    var newInput= document.createElement('input');
    newInput.setAttribute('value', salon['id']);
    newInput.setAttribute('name', 'salonID');
    var cookieInput= document.createElement('input');
    cookieInput.setAttribute('name', 'csrfmiddlewaretoken');
    cookieInput.setAttribute('value', getCookie('csrftoken'));
    form.appendChild(newInput);
    form.appendChild(cookieInput);
    document.body.appendChild(form);
    form.submit();
}

function getCookie(name) {
    // Split cookie string and get all individual name=value pairs in an array
    var cookieArr = document.cookie.split(";");
    
    // Loop through the array elements
    for(var i = 0; i < cookieArr.length; i++) {
        var cookiePair = cookieArr[i].split("=");
        
        /* Removing whitespace at the beginning of the cookie name
        and compare it with the given string */
        if(name == cookiePair[0].trim()) {
            // Decode the cookie value and return
            return decodeURIComponent(cookiePair[1]);
        }
    }
    
    // Return null if not found
    return null;
}

function disableOthers(elem) {
    var selected = elem.getAttribute('value');
    var checkboxes = document.getElementsByName('svcChkbx');
    for (chkbx of checkboxes) {
        if (chkbx.checked == true) {
            if (chkbx.getAttribute('value') != selected) {
                chkbx.checked = false;
            }
        }
    }
}

function getTimesForDate() {
    var dateInput = document.getElementById('date');
    var schedulingDiv = document.getElementById("schedulingItems");
    oldTimes = document.getElementsByName('timeInput');
    for (var oldTime of oldTimes) {
        oldTime.remove();
    }
    oldTimes = document.getElementsByName('timeInputLabel');
    for (var oldTime of oldTimes) {
        oldTime.remove();
    }
    var timeDiv = document.createElement('div');
    timeDiv.setAttribute('name', 'timeInputLabel');
    var timeSelect = document.createElement('select');
    timeSelect.setAttribute('name', 'timeInput')
    timeDiv.textContent = 'Select a time';
    schedulingDiv.appendChild(timeDiv);
    fetch('/available-times', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Cookie': document.cookie
        },
        body: JSON.stringify({ "date": dateInput.value})
    }).then((response) => response.json()).then((responseData) => {
        var enableButton = false;
        for (time of responseData) {
            console.log(time);
            var option = document.createElement('option');
            option.textContent = time['text']
            option.setAttribute('value', time['time'])
            if (time['available'] == false) {
                option.disabled = true;
            } else {
                enableButton = true;
            }
            timeSelect.appendChild(option);
        }
        schedulingDiv.appendChild(timeSelect);
        if (enableButton) {
            var nextButton = document.getElementById("nextCustomerInfo");
            nextButton.disabled = false;
        }
    }
    )
}
