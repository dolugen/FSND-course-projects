window.parseISOString = function parseISOString(s) {
  var b = s.split(/\D+/);
  return new Date(Date.UTC(b[0], --b[1], b[2], b[3], b[4], b[5], b[6]));
};

// document.getElementById('new_artist_form').onsubmit = function (e) {
//   e.preventDefault();
//   const form = document.getElementById('new_artist_form');
//   console.log(form.action);
//   fetch(form.action, {
//     method: 'POST',
//     body: JSON.stringify({
//       name: document.getElementById('name').value,
//       city: document.getElementById('city').value,
//       state: document.getElementById('state').value,
//       phone: document.getElementById('phone').value,
//       genres: document.getElementById('genres').value,
//       facebook_link: document.getElementById('facebook_link').value,
//       website: document.getElementById('website').value,
//       seeking_venue: document.getElementById('seeking_venue').value,
//       seeking_description: document.getElementById('seeking_description')
//     }),
//     headers: {
//       'Content-Type': 'application/json'
//     }
//   })
//     .then(function (response) {
//       return response.json();
//     })
//     .then(function (jsonResponse) {
//       console.log(jsonResponse);
//       // const liItem = document.createElement('li');
//       // liItem.innerHTML = jsonResponse.description;
//       // document.getElementById('todos').appendChild(liItem);
//       // document.getElementById('error').className = 'hidden';
//     })
//     .catch(function (e) {
//       console.error(e);
//     })
// }
