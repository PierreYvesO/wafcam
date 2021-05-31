import { Paper } from '@material-ui/core';
import React from 'react';
import Navigation from '../components/Navigation';

const Home = () => {
  return (
    <>
      <Navigation />
      <div className="Content">
        <h1>Accueil</h1>
        <Paper className="homeText">
          <p>
          Bienvenue dans l'application Web PatCam™,<br/><br/>
          PatCam™ à pour but de vous aidez à surveiller vos animaux de compagnie à distance.<br/><br/>
          À l'aide de caméras et de différentes options vous pourrez voir votre maison, appartement, complexe ou tout autre endroit de votre choix en temps réel. L'application est accessible de n'importe quel navigateur Web de votre choix.<br/><br/>
          PatCam™️ propose plusieurs réglages, l'application a pour rôle de suivre vos animaux en temps réel grâce à un algorithme complexe de machine learning de reconnaissance des animaux développer spécialement par nos ingénieurs. D'autres options existent notamment celle de créer des zones interdite qui, comme son nom l'indique, définissent les zones où votre animal n'as pas le droit d'aller et s'il s'y rend vous serez notifier en temps réel. L'application permet également une configuration et une personnalisation très intuitive de vos lieux / pièces disposant d'une ou de plusieurs caméras.<br/><br/>
          Ce projet a été créé et developpé par M. OUPINDRIN Pierre-Yves, M. BRASSET Alexis, M. CHEVESSIER Yoann et M. ALLAIN Joseph. PatCam™ a été pensé et conçu afin d'être le plus simple d'utilisation et le plus performant possible.<br/><br/>
          PatCam™, une nouvelle manière de dresser votre animal !<br/><br/>
          L'équipe PatCam™
          </p>
        </Paper>
        <div className="homeImgs">
          <img src="./img/PATCAM_LOGO.ico" alt="logo_patcam" width="200" />
          <img src="./img/home.png" alt="demo" width="600" />
          <img src="./img/esiee.jpg" alt="logo_esiee" width="200" />
        </div>
      </div>
    </>
  );
}
  
export default Home;
  