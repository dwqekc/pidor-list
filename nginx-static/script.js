const userList = document.getElementById('user-list');
const lgn_btn = document.getElementById('login-button');
const paginationContainer = document.getElementById('pagination');
let currentPage = 1;
let totalPages = 1;
let defaultphoto = import.meta.env.VITE_DEFAULTPHOTO;
let wsGetPidor = null;
let wsSetPidor = null;
const host=import.meta.env.VITE_HOST;
const ws_host=import.meta.env.VITE_WSHOST;

async function load_users(offset) {
  try{
    const response = await fetch(`${host}api/pidor/all_pidor?amount=10&offset=${offset}`, {
      method: "GET",
      credentials: "include"
    });
      if (response.ok){
        return response.json();
      }else{
        alert('Ошибка при попытке получить всех пользователей.Попробуйте обновить страницу');
      }
    }catch{
      alert('Ошибка при попытке получить всех пользователей.Попробуйте обновить страницу');
    };  
}

lgn_btn.addEventListener('click', function() {
  if (lgn_btn.innerText == "LOGOUT"){
    document.cookie = `Authorization=; Path=/; Domain=${window.location.hostname}; Max-Age=-1; SameSite=Lax;`;
    location.reload()
  };
  if (lgn_btn.innerHTML == "LOGIN"){
    console.log(window.location);
    window.location.href = `${window.location.origin}/login`;
  };
});

function displayUsers(users) {
  userList.innerHTML = '';
  users.forEach(user => {
    const userItem = document.createElement('li');
    userItem.id = `user-${user.id}`;
    const userContent = document.createElement('div');
    userContent.classList.add('user-info');
    const userImage = document.createElement('img');
    if (user.photo){
      userImage.classList.add('user-image');
      userImage.src = user.photo;
      userImage.alt = "Фото пользователя";
      userImage.onerror = function() {
        userImage.src = defaultphoto;
        userImage.alt = "Фото пользователя";
      };
      userContent.appendChild(userImage);
    } else{
      userImage.src = defaultphoto;
      userImage.classList.add('user-image');
      userImage.alt = "Фотография пользователя";
      userContent.appendChild(userImage);
    };
    // Добавляем информацию о пользователе справа от фотографии
    userContent.innerHTML += `
      <div class="user-details">
        <p>ID: ${user.id}</p>
        <p class="score" data-user-id="${user.id}">Pidor-Score: ${user.score}</p>
        <p>Имя: ${user.first_name}</p>
        <p>Фамилия: ${user.last_name}</p>
      </div>
    `;

    userItem.appendChild(userContent);

    // Кнопка "плюс" для увеличения скора
    const increaseScoreButton = document.createElement('button');
    increaseScoreButton.classList.add('increase-score');
    increaseScoreButton.textContent = '+';
    increaseScoreButton.addEventListener('click', () => {
      if (wsSetPidor) {
        wsSetPidor.send(user.id)
      } else {
        console.error("Websocket connection not established for setPidor");
      }
    });
    userItem.appendChild(increaseScoreButton);

    userList.appendChild(userItem);
  });
}

function updatePagination(totalUsers) {
  totalPages = Math.ceil(totalUsers / 10);
  paginationContainer.innerHTML = '';

  for (let i = 1; i <= totalPages; i++) {
    const button = document.createElement('button');
    button.textContent = i;
    button.addEventListener('click', () => {
      currentPage = i;
      load_users((currentPage - 1) * 10).then(data => {
        if (data.users && data.totalUsers) {
          displayUsers(data.users);
          updatePagination(data.totalUsers);
        };
      });
    if (i === currentPage) {
      button.classList.add('active');
    }
    paginationContainer.appendChild(button);
  });
}};

function handlePaginationClick(event) {
  if (event.target.tagName === 'BUTTON') {
    const page = parseInt(event.target.textContent);
    currentPage = page;
    load_users((currentPage - 1) * 10).then(data => {
      if (data.users && data.totalUsers) {
        displayUsers(data.users);
        updatePagination(data.totalUsers);
      };
    });    
  };
};

paginationContainer.addEventListener('click', handlePaginationClick);

window.onload = () => {
  if (document.cookie.indexOf('Authorization=') !== -1) {
    lgn_btn.style.backgroundColor = "red";
    lgn_btn.innerText = "LOGOUT";     
    console.log('sucess');
    connectToWebSockets();
    load_users(0).then(data => {
      if (data.users && data.totalUsers) {
        displayUsers(data.users);
        updatePagination(data.totalUsers);
      };
    });  
  } else {
    lgn_btn.style.backgroundColor = "green";
    let div = document.createElement('div');
    let p = document.createElement('p');
    p.innerHTML = "Привет <s>пидорас</s> пользователь,ты попал на PIDOR-LIST, суть сводится к одному: у кого больше Pidor-Score тот законченный пидорас.";
    p.style.marginBottom = "7em";
    div.appendChild(p);
    let w = document.createElement('p');
    w.innerHTML = "Для продолжения необходимо авторизоваться.";
    div.appendChild(w);
    document.body.appendChild(div); 
    lgn_btn.innerText = "LOGIN"; 
  }
};

function connectToWebSockets() {
  wsGetPidor = new WebSocket(`${ws_host}ws/pidor/getpidor`);
  wsSetPidor = new WebSocket(`${ws_host}ws/pidor/setpidor`);

  wsGetPidor.onopen = function() {
    console.log('WebSocket connection opened for getPidor');
  };
  wsGetPidor.onmessage = function(event) {
    console.log('Message received from getPidor:', event.data);
    const scoreElement = document.querySelector(`li#user-${event.data} .score`);
    if (scoreElement) {
      const currentScore = parseInt(scoreElement.textContent.split(':')[1].trim());
      scoreElement.textContent = `Pidor-Score: ${currentScore + 1}`;
    } else {
      console.error(`User with ID ${userId} not found`);
    }

  };
  wsGetPidor.onclose = function() {
    console.log('WebSocket connection closed for getPidor');
  };
  wsGetPidor.onerror = function(error) {
    console.error('WebSocket error for getPidor:', error);
  };
  wsSetPidor.onopen = function() {
    console.log('WebSocket connection opened for setPidor');
  };
  wsSetPidor.onclose = function() {
    console.log('WebSocket connection closed for setPidor');
  };
  wsSetPidor.onerror = function(error) {
    console.error('WebSocket error for setPidor:', error);
  };
};

