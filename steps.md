- `réfléchir en amont aux nombres de routes url nécessaires et à celles qu'on peut grouper en une.`
- `créer les div vide de index.html`
- `écrire le js qui affiche successivement les div suivant le lien cliqué`
- `ajouter du css montrant sur quel lien on clique actuellement`

Using Python, JavaScript, HTML, and CSS, complete the implementation of a social network that allows users to make posts, follow other users, and “like” posts. You must fulfill the following requirements:
    `New Post: Users who are signed in should be able to write a new text-based post by filling in text into a text area and then clicking a button to submit the post.`
        `The screenshot at the top of this specification shows the “New Post” box at the top of the “All Posts” page. You may choose to do this as well, or you may make the “New Post” feature a separate page.`
            - `créer un modèle pour les posts dans la bdd`
            - `créer une url menant à la vue`
            - `créer la vue pour enregistrer un post dans la bdd`
            - `dans cette vue transmettre l'objet json retourner l'ensemble des posts dans un JSON : pas sûr, c'est peut être juste la vue all posts qui doit faire ça. A réfléchir`
            - `en JS, m'assurer que si le texte est vide, on ajoute un message d'erreur et la requête n'aboutit pas`
            - `écrire la fonction JS lorsqu'on clique sur le bouton submit (fetch de cette vue)`
            - `écrire un test unitaire pour l'enregistrement d'un post (à mon avis c'est encore le client django avec post)`
            - `aller voir comment lui à écrit sa vue JS dans commerce pour m'améliorer`
    `All Posts: The “All Posts” link in the navigation bar should take the user to a page where they can see all posts from all users, with the most recent posts first.`
        `Each post should include the username of the poster, the post content itself, the date and time at which the post was made, and the number of “likes” the post has (this will be 0 for all posts until you implement the ability to “like” a post later).`
            - `écrire la vue qui génère les données`
            - `commencer par générer tous les posts même si ma fonction dépend de whichposts, on adaptera la vue pour les pages de profil et following plus tard.`
            - `bug il faut dans la json response envoyer post sous forme de json objects sinon ils ne sont pas exploitables dans les promesses.`
            - `bug : request.user.username ne semble pas passer (undefined dans l'affichage)`
            - `écrire la fonction JS pour récup les données et les afficher`
            - `changer l'ordre d'affichage des posts`
            - `scss des posts`
            - `quand je poste qqch, il faudrait que la textarea se vide et que le poste apparaisse immédiatement dessous (il semble qu'il ne rentre pas dans le fetch à l'intérieur de print someposts quand je soumets un post). On dirait qu'il ne lance pas du tout print someposts suite à submit post.`
    `Profile Page: Clicking on a username should load that user’s profile page. This page should:`
        `Display the number of followers the user has, as well as the number of people that the user follows.`
        `Display all of the posts for that user, in reverse chronological order.`
        `For any other user who is signed in, this page should also display a “Follow” or “Unfollow” button that will let the current user toggle whether or not they are following this user’s posts. Note that this only applies to any “other” user: a user should not be able to follow themselves. To verify`
            - `comprendre comment récupérer l'objet User à partir juste du username : comment est créé son objet User`
            - `créer la vue qui génère la info et la rend`
            - `ajouter un eventlst à tout bouton de classe user-btn qui fait appel à cette vue (avec la fonction JS print_profile)`
            - `on récupère l'user sur lequel on clique grâce à l'event en récupérant la valeur du bouton cliqué : écrire print profile`
            - `tests unitaires pour les vues sans post`
            - `passer à la vue aussi un booléen pour savoir si l'owner suit username.`
            - `compléter le test unitaire pour vérifier les booléens`
            - `css des boutons toto et de la page profile en entier`
            - `ajout d'un eventlistener sur ce bouton follow/unfollow`
            - `requête à soumettre à une vue si on clique sur follow, modifier la bdd dans une vue pour l'ajouter à following du request user et aux followers de celui sur lequel on clique`
            - `écrire la fonction de l'eventLst`
            - `relancer la page de profile une fois l'event Lst follow_or_unfollow fait pour voir le bouton transformé en Unfollow`
            - `test unitaire pour ça`
            - `voir pour à la fin de la requête relancer la page de profil actuelle (de l'utilisateur qu'on regardait) mise à jour : il faudra ptet mettre username à l'url profile.`
            - `css du bouton follow, le centrer`
    `Bug : `
        -` quand on se log out, les posts des utilisateurs restent affichés : est-ce ok avec les spécifications`
    `Following: The “Following” link in the navigation bar should take the user to a page where they see all posts made by users that the current user follows.`
        `This page should behave just as the “All Posts” page does, just with a more limited set of posts.`
        `This page should only be available to users who are signed in.`
            - `adapter la vue pour ne transmettre que les posts correspondants`
            - `écrire la requête en JS en cas de clic sur following`
            - `test pour faire une requête à la vue et voir si elle transmet les posts uniquement du follower.`
    `Modify to authorize the user to view all posts when not logged in`
        - `enlever le login required to print posts mais l'imposer pour la vue sur following`
        - `voir si ça tourne : accès à folliwng en étant log, et via l'url en ne l'étant pas.` 
        - `afficher l'erreur via le JS si on n'est pas logged.`
    `Pagination: On any page that displays posts, posts should only be displayed 10 on a page. If there are more than ten posts, a “Next” button should appear to take the user to the next page of posts (which should be older than the current page of posts). If not on the first page, a “Previous” button should appear to take the user to the previous page of posts as well.`
        - `je passe un entier le numéro de la page actuelle en query param dans l'url`
        - `créer un paginator de 10`
        - `on transmet l'objectlist, has previous et has next`
        - `suivant les résultats on affiche ou non un bouton next previous`
        - `test unitaire pour vérifier que 10 slt affichés`
        `See the Hints section for some suggestions on how to implement this.` 
    Edit Post: Users should be able to click an “Edit” button or link on any of their own posts to edit that post.
        When a user clicks “Edit” for one of their own posts, the content of their post should be replaced with a textarea where the user can edit the content of their post.
        The user should then be able to “Save” the edited post. Using JavaScript, you should be able to achieve this without requiring a reload of the entire page.
        For security, ensure that your application is designed such that it is not possible for a user, via any route, to edit another user’s posts.
            `ajouter un bouton edit si le post est un du request user pour Allposts et post profile`
            `factoriser index.js`
            ajouter un event listener dessus
            fonction JS qui remplace le texte par textarea contenant le précédent test et un bouton save
            event listener sur le bouton save
            écrire une vue view pour l'edition du post et la modif en bdd
            écrire la fonction JS qui fait la requête et recharge la page actuelle avec les posts mis à jour (date inchangée)
            test unitaire qui vérifie si la bdd est bien modifiée + l'envoi des bonnes données au JS.
    “Like” and “Unlike”: Users should be able to click a button or link on any post to toggle whether or not they “like” that post.
        Using JavaScript, you should asynchronously let the server know to update the like count (as via a call to fetch) and then update the post’s like count displayed on the page, without requiring a reload of the entire page.
    
    - aller voir comment lui à écrit sa vue JS dans commerce pour m'améliorer
    - Refaire ce projet en remplaçant le JS par React
