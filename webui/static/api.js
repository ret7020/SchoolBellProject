function sendForm(api_endpoint, formData){
    return fetch(api_endpoint, { 
        method: 'POST',
        body: formData
      })
      .then((response) => response.json())
      .then((responseData) => {
        return responseData;
      })
      .catch (error => console.warn(error));
}

function postReqApi(api_endpoint, data, csrf_token){
    return fetch(api_endpoint, { 
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            'X-CSRFToken': csrf_token
          }
      
      })
      .then((response) => response.json())
      .then((responseData) => {
        return responseData;
      })
      .catch (error => console.warn(error));
}

function getReqApi(api_endpoint){
    return fetch(api_endpoint)
    .then(data => {
        return data.json();
    })

}
