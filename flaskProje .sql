-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Anamakine: localhost
-- Üretim Zamanı: 28 Haz 2022, 10:56:08
-- Sunucu sürümü: 10.4.24-MariaDB
-- PHP Sürümü: 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Veritabanı: `flaskProje` create database flaskProje
--

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `cars`
--

CREATE TABLE `cars` (
  `id` int(11) NOT NULL,
  `userId` int(11) NOT NULL,
  `brand` varchar(20) NOT NULL,
  `model` varchar(20) NOT NULL,
  `year` int(11) NOT NULL,
  `km` int(11) NOT NULL,
  `damageRecord` varchar(200) NOT NULL,
  `explanation` varchar(200) NOT NULL,
  `usageTime` int(11) NOT NULL,
  `photo` varchar(25) DEFAULT NULL,
  `date` date DEFAULT current_timestamp(),
  `isReady` int(11) NOT NULL DEFAULT 0,
  `price` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Tablo döküm verisi `cars`
--



INSERT INTO `cars` (`id`, `userId`, `brand`, `model`, `year`, `km`, `damageRecord`, `explanation`, `usageTime`, `photo`, `date`, `isReady`, `price`) VALUES
(7, 15, 'peugeot', '208', 2018, 75000, 'yok', 'temiz aile aracı süper', 15, './static/15.08', '2022-05-15', 2, 275000);


-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `USERS`
--

CREATE TABLE `USERS` (
  `id` int(11) NOT NULL,
  `name` varchar(25) DEFAULT NULL,
  `surName` varchar(25) DEFAULT NULL,
  `nickName` varchar(25) DEFAULT NULL,
  `email` varchar(40) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `isAdmin` varchar(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Tablo döküm verisi `USERS`  create admin user and  password is 147258 with encryption
--

INSERT INTO `USERS` (`id`, `name`, `surName`, `nickName`, `email`, `password`, `isAdmin`) VALUES
(1, 'admin', 'admin', 'admin', 'admin@gmail.com', '7a2ec40ff8a1247c532309355f798a779e00acff579c63eec3636ffb2902c1ac', '1');



--
-- Dökümü yapılmış tablolar için indeksler
--

--
-- Tablo için indeksler `cars`
--
ALTER TABLE `cars`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_user` (`userId`);

--
-- Tablo için indeksler `USERS`
--
ALTER TABLE `USERS`
  ADD PRIMARY KEY (`id`);

--
-- Dökümü yapılmış tablolar için AUTO_INCREMENT değeri
--

--
-- Tablo için AUTO_INCREMENT değeri `cars`
--
ALTER TABLE `cars`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- Tablo için AUTO_INCREMENT değeri `USERS`
--
ALTER TABLE `USERS`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- Dökümü yapılmış tablolar için kısıtlamalar
--

--
-- Tablo kısıtlamaları `cars`
--
ALTER TABLE `cars`
  ADD CONSTRAINT `fk_user` FOREIGN KEY (`userId`) REFERENCES `USERS` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
