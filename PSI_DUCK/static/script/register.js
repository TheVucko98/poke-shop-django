// document.addEventListener('DOMContentLoaded', function() {
//     function izmeniLabele() {
//
//         const divPass1 = document.getElementById('div_id_password1');
//         divPass1.children[0].innerHTML = "Sifra*";
//         const divPass2 = document.getElementById('div_id_password2');
//         divPass2.children[0].innerHTML = "Ponovi sifru*";
//         console.log("Cao")
//
//         // Password hints
//         const hintDiv = document.getElementById('hint_id_password1');
//         if (hintDiv) {
//             // Select the ul within the div
//             const ulElement = hintDiv.querySelector('ul');
//
//             // Check if the ul exists to avoid errors
//             if (ulElement) {
//                 // Select all li elements within the ul
//                 ulElement.innerHTML = `<li>
//                                     Vaša lozinka ne može biti previše slična vašim drugim ličnim informacijama.
//                                 </li>
//                                 <li>
//                                      Vaša lozinka mora sadržati najmanje 8 karaktera.
//                                 </li>
//                                 <li>
//                                     Vaša lozinka ne može biti često korišćena lozinka.
//                                 </li>
//                                 <li>
//                                      Vaša lozinka ne može biti potpuno numerička.
//                                 </li>`
//
//
//             } else {
//                 console.log('No ul found inside the div');
//             }
//         } else {
//             console.log('No div with ID "hint_id_password1" found');
//         }
//
//         const hintUser = document.getElementById('hint_id_username');
//         hintUser.innerHTML = 'Obavezno. 150 karaktera ili manje. Dozvoljena slova, cifre i @/./+/-/_.'
//
//         const hintPass2 = document.getElementById('hint_id_password2');
//         hintPass2.innerHTML = 'Unesite istu lozinku kao ranije, za verifikaciju.'
//     }
//     izmeniLabele()
//
// });