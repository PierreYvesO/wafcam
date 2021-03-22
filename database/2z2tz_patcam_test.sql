-- phpMyAdmin SQL Dump
-- version 4.9.2
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le :  lun. 22 mars 2021 à 14:29
-- Version du serveur :  10.4.10-MariaDB
-- Version de PHP :  7.3.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données :  `2z2tz_patcam_test`
--

-- --------------------------------------------------------

--
-- Structure de la table `camera`
--

DROP TABLE IF EXISTS `camera`;
CREATE TABLE IF NOT EXISTS `camera` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `ip` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ip` (`ip`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `camera`
--

INSERT INTO `camera` (`id`, `name`, `ip`) VALUES
(1, 'camera_1', '192.168.1.1'),
(2, 'camera_2', '192.168.1.2'),
(3, 'camera_3', '192.168.1.3');

-- --------------------------------------------------------

--
-- Structure de la table `entity`
--

DROP TABLE IF EXISTS `entity`;
CREATE TABLE IF NOT EXISTS `entity` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `entity`
--

INSERT INTO `entity` (`id`, `name`) VALUES
(1, 'entity_1'),
(2, 'entity_2'),
(3, 'entity_3');

-- --------------------------------------------------------

--
-- Structure de la table `forbidden_area`
--

DROP TABLE IF EXISTS `forbidden_area`;
CREATE TABLE IF NOT EXISTS `forbidden_area` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `room_id` int(11) NOT NULL,
  `position_x` int(11) NOT NULL,
  `position_y` int(11) NOT NULL,
  `width` int(11) NOT NULL,
  `height` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `forbidden_area_room_id` (`room_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

--
-- Déchargement des données de la table `forbidden_area`
--

INSERT INTO `forbidden_area` (`id`, `room_id`, `position_x`, `position_y`, `width`, `height`) VALUES
(1, 1, 100, 100, 100, 100),
(2, 2, 200, 200, 200, 200),
(3, 3, 300, 300, 300, 300);

-- --------------------------------------------------------

--
-- Structure de la table `room`
--

DROP TABLE IF EXISTS `room`;
CREATE TABLE IF NOT EXISTS `room` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `camera_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `room_camera_id` (`camera_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `room`
--

INSERT INTO `room` (`id`, `name`, `camera_id`) VALUES
(1, 'room_1', 1),
(2, 'room_2', 2),
(3, 'room_3', 3);

-- --------------------------------------------------------

--
-- Structure de la table `room_entities`
--

DROP TABLE IF EXISTS `room_entities`;
CREATE TABLE IF NOT EXISTS `room_entities` (
  `room_id` int(11) NOT NULL,
  `entity_id` int(11) NOT NULL,
  `amount_entities` int(11) NOT NULL,
  `time_record` datetime NOT NULL,
  KEY `room_entities_entity_id` (`entity_id`),
  KEY `room_entities_room_id` (`room_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `room_entities`
--

INSERT INTO `room_entities` (`room_id`, `entity_id`, `amount_entities`, `time_record`) VALUES
(1, 1, 10, '2021-03-22 00:00:00'),
(2, 2, 15, '2021-03-22 00:00:00'),
(3, 3, 20, '2021-03-22 00:00:00');

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `forbidden_area`
--
ALTER TABLE `forbidden_area`
  ADD CONSTRAINT `forbidden_area_room_id` FOREIGN KEY (`room_id`) REFERENCES `room` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Contraintes pour la table `room`
--
ALTER TABLE `room`
  ADD CONSTRAINT `room_camera_id` FOREIGN KEY (`camera_id`) REFERENCES `camera` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Contraintes pour la table `room_entities`
--
ALTER TABLE `room_entities`
  ADD CONSTRAINT `room_entities_entity_id` FOREIGN KEY (`entity_id`) REFERENCES `entity` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `room_entities_room_id` FOREIGN KEY (`room_id`) REFERENCES `room` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
