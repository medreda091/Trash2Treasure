// Inscription utilisateur
document.getElementById('inscription-form').addEventListener('submit', function(event) {
    event.preventDefault();

    let nom = document.getElementById('nom').value;
    let email = document.getElementById('email').value;
    let mot_de_passe = document.getElementById('mot_de_passe').value;

    fetch('http://127.0.0.1:5000/inscription', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            nom: nom,
            email: email,
            mot_de_passe: mot_de_passe
        })
    })
    .then(response => response.json())
    .then(data => alert(data.message))
    .catch(error => console.error('Erreur:', error));
});

// Connexion utilisateur
document.getElementById('connexion-form').addEventListener('submit', function(event) {
    event.preventDefault();

    let email = document.getElementById('email').value;
    let mot_de_passe = document.getElementById('mot_de_passe').value;

    fetch('http://127.0.0.1:5000/connexion', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            email: email,
            mot_de_passe: mot_de_passe
        })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        if (data.utilisateur_id) {
            // Sauvegarder l'ID utilisateur dans localStorage ou sessionStorage si nécessaire
            localStorage.setItem('utilisateur_id', data.utilisateur_id);
        }
    })
    .catch(error => console.error('Erreur:', error));
});

// Récupérer et afficher les annonces
window.onload = function() {
    fetch('http://127.0.0.1:5000/annonces')
        .then(response => response.json())
        .then(annonces => {
            const annoncesList = document.getElementById('annonces-list');
            annonces.forEach(annonce => {
                let div = document.createElement('div');
                div.innerHTML = `
                    <h3>${annonce.titre}</h3>
                    <p>${annonce.description}</p>
                    <p>${annonce.prix ? annonce.prix : 'Gratuit'}</p>
                `;
                annoncesList.appendChild(div);
            });
        })
        .catch(error => console.error('Erreur:', error));
};

// Envoi de message
document.getElementById('envoyer-message-form').addEventListener('submit', function(event) {
    event.preventDefault();

    let contenu = document.getElementById('contenu').value;
    let utilisateur_id_envoyeur = localStorage.getItem('utilisateur_id');  // Récupérer l'utilisateur connecté
    let utilisateur_id_destinataire = document.getElementById('utilisateur_id_destinataire').value;

    fetch('http://127.0.0.1:5000/message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            contenu: contenu,
            utilisateur_id_envoyeur: utilisateur_id_envoyeur,
            utilisateur_id_destinataire: utilisateur_id_destinataire
        })
    })
    .then(response => response.json())
    .then(data => alert(data.message))
    .catch(error => console.error('Erreur:', error));
});

// Récupérer et afficher les messages d'un utilisateur
function getMessages(utilisateur_id) {
    fetch(`http://127.0.0.1:5000/messages/${utilisateur_id}`)
        .then(response => response.json())
        .then(messages => {
            const messagesList = document.getElementById('messages-list');
            messagesList.innerHTML = ''; // Vide la liste avant d'afficher
            messages.forEach(message => {
                let div = document.createElement('div');
                div.innerHTML = `
                    <p><strong>${message.utilisateur_envoyeur} → ${message.utilisateur_destinataire}</strong>: ${message.contenu}</p>
                    <p><em>${message.date_envoi}</em></p>
                `;
                messagesList.appendChild(div);
            });
        })
        .catch(error => console.error('Erreur:', error));
}

// Appeler la fonction pour récupérer les messages d'un utilisateur après connexion
document.addEventListener('DOMContentLoaded', function() {
    let utilisateur_id = localStorage.getItem('utilisateur_id');
    if (utilisateur_id) {
        getMessages(utilisateur_id);
    }
});
