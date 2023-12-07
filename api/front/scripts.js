/*
  --------------------------------------------------------------------------------------
  Função para obter a lista existente do servidor via requisição GET
  --------------------------------------------------------------------------------------
*/
const getList = async () => {
  let url = 'http://127.0.0.1:5000/usuarios';
  fetch(url, {
    method: 'get',
  })
    .then((response) => response.json())
    .then((data) => {
      data.usuarios.forEach(item => insertList(item.name,
                                                item.userid, 
                                                item.age, 
                                                item.estimatedsalary,
                                                item.gender,
                                                item.purchased,
                                              ))
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

/*
  --------------------------------------------------------------------------------------
  Chamada da função para carregamento inicial dos dados
  --------------------------------------------------------------------------------------
*/
getList()




/*
  --------------------------------------------------------------------------------------
  Função para colocar um item na lista do servidor via requisição POST
  --------------------------------------------------------------------------------------
*/
const postItem = async (inputUsuario, inputUserID, inputAge, inputEstimatedSalary,
                        inputGender) => {
    
  const formData = new FormData();
  formData.append('name', inputUsuario);
  formData.append('userid', inputUserID);
  formData.append('age', inputAge);
  formData.append('estimatedsalary', inputEstimatedSalary);
  formData.append('gender', inputGender);
  

  let url = 'http://127.0.0.1:5000/usuario';
  fetch(url, {
    method: 'post',
    body: formData
  })
    .then((response) => response.json())
    .catch((error) => {
      console.error('Error:', error);
    });
}


/*
  --------------------------------------------------------------------------------------
  Função para criar um botão close para cada item da lista
  --------------------------------------------------------------------------------------
*/
const insertDeleteButton = (parent) => {
  let span = document.createElement("span");
  let txt = document.createTextNode("\u00D7");
  span.className = "close";
  span.appendChild(txt);
  parent.appendChild(span);
}

/*
  --------------------------------------------------------------------------------------
  Função para remover um item da lista de acordo com o click no botão close
  --------------------------------------------------------------------------------------
*/
const removeElement = () => {
  let close = document.getElementsByClassName("close");
  // var table = document.getElementById('myTable');
  let i;
  for (i = 0; i < close.length; i++) {
    close[i].onclick = function () {
      let div = this.parentElement.parentElement;
      const nomeItem = div.getElementsByTagName('td')[0].innerHTML
      if (confirm("Você tem certeza?")) {
        div.remove()
        deleteItem(nomeItem)
        alert("Removido!")
      }
    }
  }
}

/*
  --------------------------------------------------------------------------------------
  Função para deletar um item da lista do servidor via requisição DELETE
  --------------------------------------------------------------------------------------
*/
const deleteItem = (item) => {
  console.log(item)
  let url = 'http://127.0.0.1:5000/usuario?name='+item;
  fetch(url, {
    method: 'delete'
  })
    .then((response) => response.json())
    .catch((error) => {
      console.error('Error:', error);
    });
}

/*
  --------------------------------------------------------------------------------------
  Função para adicionar um novo item com nome, quantidade e valor 
  --------------------------------------------------------------------------------------
*/
const newItem = async () => {
  let inputUsuario = document.getElementById("newInput").value;
  let inputUserID = document.getElementById("newUserID").value;
  let inputAge = document.getElementById("newAge").value;
  let inputEstimatedSalary= document.getElementById("newEstimatedSalary").value;
  let inputGender = document.getElementById("newGender").value;
  

  // Verifique se o nome do usuário já existe antes de adicionar
  const checkUrl = `http://127.0.0.1:5000/usuarios?nome=${inputUsuario}`;
  fetch(checkUrl, {
    method: 'get'
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.usuarios && data.usuarios.some(item => item.name === inputUsuario)) {
        alert("O paciente já está cadastrado.\nCadastre o paciente com um nome diferente ou atualize o existente.");
      } else if (inputUsuario === '') {
        alert("O nome do paciente não pode ser vazio!");
      } else if (isNaN(inputUserID) || isNaN(inputAge) || isNaN(inputEstimatedSalary) || isNaN(inputGender)) {
        alert("Esse(s) campo(s) precisam ser números!");
      } else {
        insertList(inputUsuario, inputUserID, inputAge, inputEstimatedSalary, inputGender);
        postItem(inputUsuario, inputUserID, inputAge, inputEstimatedSalary, inputGender);
        alert("Item adicionado!");
      }
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}


/*
  --------------------------------------------------------------------------------------
  Função para inserir items na lista apresentada
  --------------------------------------------------------------------------------------
*/
const insertList = (nameUsuario, userid, age, estimatedSalary, gender, purchased) => {
  var item = [nameUsuario, userid, age, estimatedSalary, gender, purchased];
  var table = document.getElementById('myTable');
  var row = table.insertRow();

  for (var i = 0; i < item.length; i++) {
    var cell = row.insertCell(i);
    cell.textContent = item[i];
  }

  var deleteCell = row.insertCell(-1);
  insertDeleteButton(deleteCell);

  document.getElementById("newInput").value = "";
  document.getElementById("newUserID").value = "";
  document.getElementById("newAge").value = "";
  document.getElementById("newEstimatedSalary").value = "";
  document.getElementById("newGender").value = "";

  removeElement();
}