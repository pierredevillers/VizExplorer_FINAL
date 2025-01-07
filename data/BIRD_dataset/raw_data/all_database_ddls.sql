-- DDLs for Database: academic --
-- DDLs for Database: california_schools --
-- public.satscores --
-- Table definition
CREATE TABLE public.satscores (cds character varying ,rtype character varying ,sname character varying ,dname character varying ,cname character varying ,enroll12 integer ,"NumTstTakr" integer ,"AvgScrRead" integer ,"AvgScrMath" integer ,"AvgScrWrite" integer ,"NumGE1500" integer )

-- public.schools --
-- Table definition
CREATE TABLE public.schools ("CDSCode" character varying ,"NCESDist" character varying ,"NCESSchool" character varying ,"StatusType" character varying ,"County" character varying ,"District" character varying ,"School" character varying ,"Street" character varying ,"StreetAbr" character varying ,"City" character varying ,"Zip" character varying ,"State" character varying ,"MailStreet" character varying ,"MailStrAbr" character varying ,"MailCity" character varying ,"MailZip" character varying ,"MailState" character varying ,"Phone" character varying ,"Ext" character varying ,"Website" character varying ,"OpenDate" date ,"ClosedDate" date ,"Charter" integer ,"CharterNum" character varying ,"FundingType" character varying ,"DOC" character varying ,"DOCType" character varying ,"SOC" character varying ,"SOCType" character varying ,"EdOpsCode" character varying ,"EdOpsName" character varying ,"EILCode" character varying ,"EILName" character varying ,"GSoffered" character varying ,"GSserved" character varying ,"Virtual" character varying ,"Magnet" integer ,"Latitude" real ,"Longitude" real ,"AdmFName1" character varying ,"AdmLName1" character varying ,"AdmEmail1" character varying ,"AdmFName2" character varying ,"AdmLName2" character varying ,"AdmEmail2" character varying ,"AdmFName3" character varying ,"AdmLName3" character varying ,"AdmEmail3" character varying ,"LastUpdate" date )

-- Constraints
ALTER TABLE public.schools ADD CONSTRAINT unique_cdscode UNIQUE ("CDSCode")



-- public.frpm --
-- Table definition
CREATE TABLE public.frpm ("CDSCode" character varying ,"Academic Year" character varying ,"County Code" character varying ,"District Code" integer ,"School Code" character varying ,"County Name" character varying ,"District Name" character varying ,"School Name" character varying ,"District Type" character varying ,"School Type" character varying ,"Educational Option Type" character varying ,"NSLP Provision Status" character varying ,"Charter School (Y/N)" integer ,"Charter School Number" character varying ,"Charter Funding Type" character varying ,"IRC" integer ,"Low Grade" character varying ,"High Grade" character varying ,"Enrollment (K-12)" real ,"Free Meal Count (K-12)" real ,"Percent (%) Eligible Free (K-12)" real ,"FRPM Count (K-12)" real ,"Percent (%) Eligible FRPM (K-12)" real ,"Enrollment (Ages 5-17)" real ,"Free Meal Count (Ages 5-17)" real ,"Percent (%) Eligible Free (Ages 5-17)" real ,"FRPM Count (Ages 5-17)" real ,"Percent (%) Eligible FRPM (Ages 5-17)" real ,"2013-14 CALPADS Fall 1 Certification Status" integer )

-- DDLs for Database: card_games --
-- public.cards --
-- Table definition
CREATE TABLE public.cards (id integer ,artist character varying ,"asciiName" character varying ,availability character varying ,"borderColor" character varying ,"cardKingdomFoilId" character varying ,"cardKingdomId" character varying ,"colorIdentity" character varying ,"colorIndicator" character varying ,colors character varying ,"convertedManaCost" real ,"duelDeck" character varying ,"edhrecRank" integer ,"faceConvertedManaCost" real ,"faceName" character varying ,"flavorName" character varying ,"flavorText" character varying ,"frameEffects" character varying ,"frameVersion" character varying ,hand character varying ,"hasAlternativeDeckLimit" integer ,"hasContentWarning" integer ,"hasFoil" integer ,"hasNonFoil" integer ,"isAlternative" integer ,"isFullArt" integer ,"isOnlineOnly" integer ,"isOversized" integer ,"isPromo" integer ,"isReprint" integer ,"isReserved" integer ,"isStarter" integer ,"isStorySpotlight" integer ,"isTextless" integer ,"isTimeshifted" integer ,keywords character varying ,layout character varying ,"leadershipSkills" character varying ,life character varying ,loyalty character varying ,"manaCost" character varying ,"mcmId" character varying ,"mcmMetaId" character varying ,"mtgArenaId" character varying ,"mtgjsonV4Id" character varying ,"mtgoFoilId" character varying ,"mtgoId" character varying ,"multiverseId" character varying ,name character varying ,number character varying ,"originalReleaseDate" character varying ,"originalText" character varying ,"originalType" character varying ,"otherFaceIds" character varying ,power character varying ,printings character varying ,"promoTypes" character varying ,"purchaseUrls" character varying ,rarity character varying ,"scryfallId" character varying ,"scryfallIllustrationId" character varying ,"scryfallOracleId" character varying ,"setCode" character varying ,side character varying ,subtypes character varying ,supertypes character varying ,"tcgplayerProductId" character varying ,text character varying ,toughness character varying ,type character varying ,types character varying ,uuid character varying ,variations character varying ,watermark character varying )

-- public.foreign_data --
-- Table definition
CREATE TABLE public.foreign_data (id integer ,"flavorText" character varying ,language character varying ,multiverseid integer ,name character varying ,text character varying ,type character varying ,uuid character varying )

-- public.legalities --
-- Table definition
CREATE TABLE public.legalities (id integer ,format character varying ,status character varying ,uuid character varying )

-- public.sets --
-- Table definition
CREATE TABLE public.sets (id integer ,"baseSetSize" integer ,block character varying ,booster character varying ,code character varying ,"isFoilOnly" integer ,"isForeignOnly" integer ,"isNonFoilOnly" integer ,"isOnlineOnly" integer ,"isPartialPreview" integer ,"keyruneCode" character varying ,"mcmId" integer ,"mcmIdExtras" integer ,"mcmName" character varying ,"mtgoCode" character varying ,name character varying ,"parentCode" character varying ,"releaseDate" date ,"tcgplayerGroupId" integer ,"totalSetSize" integer ,type character varying )

-- public.set_translations --
-- Table definition
CREATE TABLE public.set_translations (id integer ,language character varying ,"setCode" character varying ,translation character varying )

-- public.rulings --
-- Table definition
CREATE TABLE public.rulings (id integer ,date date ,text character varying ,uuid character varying )

-- DDLs for Database: codebase_community --
-- public.badges --
-- Table definition
CREATE TABLE public.badges ("Id" integer ,"UserId" integer ,"Name" character varying ,"Date" timestamp without time zone )

-- public.comments --
-- Table definition
CREATE TABLE public.comments ("Id" integer ,"PostId" integer ,"Score" integer ,"Text" character varying ,"CreationDate" timestamp without time zone ,"UserId" integer ,"UserDisplayName" character varying )

-- public.postHistory --
-- Table definition
CREATE TABLE public."postHistory" ("Id" integer ,"PostHistoryTypeId" integer ,"PostId" integer ,"RevisionGUID" character varying ,"CreationDate" timestamp without time zone ,"UserId" integer ,"Text" character varying ,"Comment" character varying ,"UserDisplayName" character varying )

-- public.postLinks --
-- Table definition
CREATE TABLE public."postLinks" ("Id" integer ,"CreationDate" timestamp without time zone ,"PostId" integer ,"RelatedPostId" integer ,"LinkTypeId" integer )

-- public.posts --
-- Table definition
CREATE TABLE public.posts ("Id" integer ,"PostTypeId" integer ,"AcceptedAnswerId" integer ,"CreaionDate" timestamp without time zone ,"Score" integer ,"ViewCount" integer ,"Body" character varying ,"OwnerUserId" integer ,"LasActivityDate" timestamp without time zone ,"Title" character varying ,"Tags" character varying ,"AnswerCount" integer ,"CommentCount" integer ,"FavoriteCount" integer ,"LastEditorUserId" integer ,"LastEditDate" timestamp without time zone ,"CommunityOwnedDate" timestamp without time zone ,"ParentId" integer ,"ClosedDate" timestamp without time zone ,"OwnerDisplayName" character varying ,"LastEditorDisplayName" character varying )

-- public.tags --
-- Table definition
CREATE TABLE public.tags ("Id" integer ,"TagName" character varying ,"Count" integer ,"ExcerptPostId" integer ,"WikiPostId" integer )

-- public.users --
-- Table definition
CREATE TABLE public.users ("Id" integer ,"Reputation" integer ,"CreationDate" timestamp without time zone ,"DisplayName" character varying ,"LastAccessDate" timestamp without time zone ,"WebsiteUrl" character varying ,"Location" character varying ,"AboutMe" character varying ,"Views" integer ,"UpVotes" integer ,"DownVotes" integer ,"AccountId" integer ,"Age" integer ,"ProfileImageUrl" character varying )

-- public.votes --
-- Table definition
CREATE TABLE public.votes ("Id" integer ,"PostId" integer ,"VoteTypeId" integer ,"CreationDate" date ,"UserId" integer ,"BountyAmount" integer )

-- DDLs for Database: debit_card_specializing --
-- public.customers --
-- Table definition
CREATE TABLE public.customers ("CustomerID" integer ,"Segment" character varying ,"Currency" character varying )

-- public.gasstations --
-- Table definition
CREATE TABLE public.gasstations ("GasStationID" integer ,"ChainID" integer ,"Country" character varying ,"Segment" character varying )

-- public.products --
-- Table definition
CREATE TABLE public.products ("ProductID" integer ,"Description" character varying )

-- public.transactions_1k --
-- Table definition
CREATE TABLE public.transactions_1k ("TransactionID" integer ,"Date" date ,"Time" character varying ,"CustomerID" integer ,"CardID" integer ,"GasStationID" integer ,"ProductID" integer ,"Amount" integer ,"Price" real )

-- public.yearmonth --
-- Table definition
CREATE TABLE public.yearmonth ("CustomerID" integer ,"Date" character varying ,"Consumption" real )

-- DDLs for Database: european_football_2 --
-- public.Player_Attributes --
-- Table definition
CREATE TABLE public."Player_Attributes" (id integer ,player_fifa_api_id integer ,player_api_id integer ,date character varying ,overall_rating integer ,potential integer ,preferred_foot character varying ,attacking_work_rate character varying ,defensive_work_rate character varying ,crossing integer ,finishing integer ,heading_accuracy integer ,short_passing integer ,volleys integer ,dribbling integer ,curve integer ,free_kick_accuracy integer ,long_passing integer ,ball_control integer ,acceleration integer ,sprint_speed integer ,agility integer ,reactions integer ,balance integer ,shot_power integer ,jumping integer ,stamina integer ,strength integer ,long_shots integer ,aggression integer ,interceptions integer ,positioning integer ,vision integer ,penalties integer ,marking integer ,standing_tackle integer ,sliding_tackle integer ,gk_diving integer ,gk_handling integer ,gk_kicking integer ,gk_positioning integer ,gk_reflexes integer )

-- public.Player --
-- Table definition
CREATE TABLE public."Player" (id integer ,player_api_id integer ,player_name character varying ,player_fifa_api_id integer ,birthday character varying ,height integer ,weight integer )

-- public.League --
-- Table definition
CREATE TABLE public."League" (id integer ,country_id integer ,name character varying )

-- public.Country --
-- Table definition
CREATE TABLE public."Country" (id integer ,name character varying )

-- public.Team --
-- Table definition
CREATE TABLE public."Team" (id integer ,team_api_id integer ,team_fifa_api_id integer ,team_long_name character varying ,team_short_name character varying )

-- public.Team_Attributes --
-- Table definition
CREATE TABLE public."Team_Attributes" (id integer ,team_fifa_api_id integer ,team_api_id integer ,date character varying ,"buildUpPlaySpeed" integer ,"buildUpPlaySpeedClass" character varying ,"buildUpPlayDribbling" integer ,"buildUpPlayDribblingClass" character varying ,"buildUpPlayPassing" integer ,"buildUpPlayPassingClass" character varying ,"buildUpPlayPositioningClass" character varying ,"chanceCreationPassing" integer ,"chanceCreationPassingClass" character varying ,"chanceCreationCrossing" integer ,"chanceCreationCrossingClass" character varying ,"chanceCreationShooting" integer ,"chanceCreationShootingClass" character varying ,"chanceCreationPositioningClass" character varying ,"defencePressure" integer ,"defencePressureClass" character varying ,"defenceAggression" integer ,"defenceAggressionClass" character varying ,"defenceTeamWidth" integer ,"defenceTeamWidthClass" character varying ,"defenceDefenderLineClass" character varying )

-- public.Match --
-- Table definition
CREATE TABLE public."Match" (id integer ,country_id integer ,league_id integer ,season character varying ,stage integer ,date character varying ,match_api_id integer ,home_team_api_id integer ,away_team_api_id integer ,home_team_goal integer ,away_team_goal integer ,"home_player_X1" integer ,"home_player_X2" integer ,"home_player_X3" integer ,"home_player_X4" integer ,"home_player_X5" integer ,"home_player_X6" integer ,"home_player_X7" integer ,"home_player_X8" integer ,"home_player_X9" integer ,"home_player_X10" integer ,"home_player_X11" integer ,"away_player_X1" integer ,"away_player_X2" integer ,"away_player_X3" integer ,"away_player_X4" integer ,"away_player_X5" integer ,"away_player_X6" integer ,"away_player_X7" integer ,"away_player_X8" integer ,"away_player_X9" integer ,"away_player_X10" integer ,"away_player_X11" integer ,"home_player_Y1" integer ,"home_player_Y2" integer ,"home_player_Y3" integer ,"home_player_Y4" integer ,"home_player_Y5" integer ,"home_player_Y6" integer ,"home_player_Y7" integer ,"home_player_Y8" integer ,"home_player_Y9" integer ,"home_player_Y10" integer ,"home_player_Y11" integer ,"away_player_Y1" integer ,"away_player_Y2" integer ,"away_player_Y3" integer ,"away_player_Y4" integer ,"away_player_Y5" integer ,"away_player_Y6" integer ,"away_player_Y7" integer ,"away_player_Y8" integer ,"away_player_Y9" integer ,"away_player_Y10" integer ,"away_player_Y11" integer ,home_player_1 integer ,home_player_2 integer ,home_player_3 integer ,home_player_4 integer ,home_player_5 integer ,home_player_6 integer ,home_player_7 integer ,home_player_8 integer ,home_player_9 integer ,home_player_10 integer ,home_player_11 integer ,away_player_1 integer ,away_player_2 integer ,away_player_3 integer ,away_player_4 integer ,away_player_5 integer ,away_player_6 integer ,away_player_7 integer ,away_player_8 integer ,away_player_9 integer ,away_player_10 integer ,away_player_11 integer ,goal character varying ,shoton character varying ,shotoff character varying ,foulcommit character varying ,card character varying ,"cross" character varying ,corner character varying ,possession character varying ,"B365H" real ,"B365D" real ,"B365A" real ,"BWH" real ,"BWD" real ,"BWA" real ,"IWH" real ,"IWD" real ,"IWA" real ,"LBH" real ,"LBD" real ,"LBA" real ,"PSH" real ,"PSD" real ,"PSA" real ,"WHH" real ,"WHD" real ,"WHA" real ,"SJH" real ,"SJD" real ,"SJA" real ,"VCH" real ,"VCD" real ,"VCA" real ,"GBH" real ,"GBD" real ,"GBA" real ,"BSH" real ,"BSD" real ,"BSA" real )

-- DDLs for Database: financial --
-- public.account --
-- Table definition
CREATE TABLE public.account (account_id integer ,district_id integer ,frequency character varying ,date date )

-- public.card --
-- Table definition
CREATE TABLE public.card (card_id integer ,disp_id integer ,type character varying ,issued date )

-- public.client --
-- Table definition
CREATE TABLE public.client (client_id integer ,gender character varying ,birth_date date ,district_id integer )

-- public.disp --
-- Table definition
CREATE TABLE public.disp (disp_id integer ,client_id integer ,account_id integer ,type character varying )

-- public.district --
-- Table definition
CREATE TABLE public.district (district_id integer ,"A2" character varying ,"A3" character varying ,"A4" character varying ,"A5" character varying ,"A6" character varying ,"A7" character varying ,"A8" integer ,"A9" integer ,"A10" real ,"A11" integer ,"A12" real ,"A13" real ,"A14" integer ,"A15" integer ,"A16" integer )

-- public.loan --
-- Table definition
CREATE TABLE public.loan (loan_id integer ,account_id integer ,date date ,amount integer ,duration integer ,payments real ,status character varying )

-- DDLs for Database: formula_1 --
-- public.circuits --
-- Table definition
CREATE TABLE public.circuits ("circuitId" integer ,"circuitRef" character varying ,name character varying ,location character varying ,country character varying ,lat real ,lng real ,alt integer ,url character varying )

-- public.constructors --
-- Table definition
CREATE TABLE public.constructors ("constructorId" integer ,"constructorRef" character varying ,name character varying ,nationality character varying ,url character varying )

-- public.drivers --
-- Table definition
CREATE TABLE public.drivers ("driverId" integer ,"driverRef" character varying ,number integer ,code character varying ,forename character varying ,surname character varying ,dob date ,nationality character varying ,url character varying )

-- public.seasons --
-- Table definition
CREATE TABLE public.seasons (year integer ,url character varying )

-- public.races --
-- Table definition
CREATE TABLE public.races ("raceId" integer ,year integer ,round integer ,"circuitId" integer ,name character varying ,date date ,"time" character varying ,url character varying )

-- public.constructorResults --
-- Table definition
CREATE TABLE public."constructorResults" ("constructorResultsId" integer ,"raceId" integer ,"constructorId" integer ,points real ,status character varying )

-- public.constructorStandings --
-- Table definition
CREATE TABLE public."constructorStandings" ("constructorStandingsId" integer ,"raceId" integer ,"constructorId" integer ,points real ,"position" integer ,"positionText" character varying ,wins integer )

-- public.driverStandings --
-- Table definition
CREATE TABLE public."driverStandings" ("driverStandingsId" integer ,"raceId" integer ,"driverId" integer ,points real ,"position" integer ,"positionText" character varying ,wins integer )

-- public.lapTimes --
-- Table definition
CREATE TABLE public."lapTimes" ("raceId" integer ,"driverId" integer ,lap integer ,"position" integer ,"time" character varying ,milliseconds integer )

-- public.pitStops --
-- Table definition
CREATE TABLE public."pitStops" ("raceId" integer ,"driverId" integer ,stop integer ,lap integer ,"time" character varying ,duration character varying ,milliseconds integer )

-- public.qualifying --
-- Table definition
CREATE TABLE public.qualifying ("qualifyId" integer ,"raceId" integer ,"driverId" integer ,"constructorId" integer ,number integer ,"position" integer ,q1 character varying ,q2 character varying ,q3 character varying )

-- public.status --
-- Table definition
CREATE TABLE public.status ("statusId" integer ,status character varying )

-- public.results --
-- Table definition
CREATE TABLE public.results ("resultId" integer ,"raceId" integer ,"driverId" integer ,"constructorId" integer ,number integer ,grid integer ,"position" integer ,"positionText" character varying ,"positionOrder" integer ,points real ,laps integer ,"time" character varying ,milliseconds integer ,"fastestLap" integer ,rank integer ,"fastestLapTime" character varying ,"fastestLapSpeed" character varying ,"statusId" integer )

-- DDLs for Database: student_club --
-- public.event --
-- Table definition
CREATE TABLE public.event (event_id character varying ,event_name character varying ,event_date character varying ,type character varying ,notes character varying ,location character varying ,status character varying )

-- public.major --
-- Table definition
CREATE TABLE public.major (major_id character varying ,major_name character varying ,department character varying ,college character varying )

-- public.zip_code --
-- Table definition
CREATE TABLE public.zip_code (zip_code integer ,type character varying ,city character varying ,county character varying ,state character varying ,short_state character varying )

-- public.attendance --
-- Table definition
CREATE TABLE public.attendance (link_to_event character varying ,link_to_member character varying )

-- public.budget --
-- Table definition
CREATE TABLE public.budget (budget_id character varying ,category character varying ,spent real ,remaining real ,amount integer ,event_status character varying ,link_to_event character varying )

-- public.expense --
-- Table definition
CREATE TABLE public.expense (expense_id character varying ,expense_description character varying ,expense_date character varying ,cost real ,approved character varying ,link_to_member character varying ,link_to_budget character varying )

-- public.income --
-- Table definition
CREATE TABLE public.income (income_id character varying ,date_received character varying ,amount integer ,source character varying ,notes character varying ,link_to_member character varying )

-- public.member --
-- Table definition
CREATE TABLE public.member (member_id character varying ,first_name character varying ,last_name character varying ,email character varying ,"position" character varying ,t_shirt_size character varying ,phone character varying ,zip integer ,link_to_major character varying )

-- DDLs for Database: superhero --
-- public.alignment --
-- Table definition
CREATE TABLE public.alignment (id integer ,alignment character varying )

-- public.attribute --
-- Table definition
CREATE TABLE public.attribute (id integer ,attribute_name character varying )

-- public.colour --
-- Table definition
CREATE TABLE public.colour (id integer ,colour character varying )

-- public.gender --
-- Table definition
CREATE TABLE public.gender (id integer ,gender character varying )

-- public.publisher --
-- Table definition
CREATE TABLE public.publisher (id integer ,publisher_name character varying )

-- public.race --
-- Table definition
CREATE TABLE public.race (id integer ,race character varying )

-- public.superhero --
-- Table definition
CREATE TABLE public.superhero (id integer ,superhero_name character varying ,full_name character varying ,gender_id integer ,eye_colour_id integer ,hair_colour_id integer ,skin_colour_id integer ,race_id integer ,publisher_id integer ,alignment_id integer ,height_cm integer ,weight_kg integer )

-- public.hero_attribute --
-- Table definition
CREATE TABLE public.hero_attribute (hero_id integer ,attribute_id integer ,attribute_value integer )

-- public.superpower --
-- Table definition
CREATE TABLE public.superpower (id integer ,power_name character varying )

-- public.hero_power --
-- Table definition
CREATE TABLE public.hero_power (hero_id integer ,power_id integer )

-- DDLs for Database: thrombosis_prediction --
-- public.Examination --
-- Table definition
CREATE TABLE public."Examination" ("ID" integer ,"Examination Date" date ,"aCL IgG" real ,"aCL IgM" real ,"ANA" integer ,"ANA Pattern" character varying ,"aCL IgA" integer ,"Diagnosis" character varying ,"KCT" character varying ,"RVVT" character varying ,"LAC" character varying ,"Symptoms" character varying ,"Thrombosis" integer )

-- public.Patient --
-- Table definition
CREATE TABLE public."Patient" ("ID" integer ,"SEX" character varying ,"Birthday" date ,"Description" date ,"First Date" date ,"Admission" character varying ,"Diagnosis" character varying )

-- public.Laboratory --
-- Table definition
CREATE TABLE public."Laboratory" ("ID" integer ,"Date" date ,"GOT" integer ,"GPT" integer ,"LDH" integer ,"ALP" integer ,"TP" real ,"ALB" real ,"UA" real ,"UN" integer ,"CRE" real ,"T-BIL" real ,"T-CHO" integer ,"TG" integer ,"CPK" integer ,"GLU" integer ,"WBC" real ,"RBC" real ,"HGB" real ,"HCT" real ,"PLT" integer ,"PT" real ,"APTT" integer ,"FG" real ,"PIC" integer ,"TAT" integer ,"TAT2" integer ,"U-PRO" character varying ,"IGG" integer ,"IGA" integer ,"IGM" integer ,"CRP" character varying ,"RA" character varying ,"RF" character varying ,"C3" integer ,"C4" integer ,"RNP" character varying ,"SM" character varying ,"SC170" character varying ,"SSA" character varying ,"SSB" character varying ,"CENTROMEA" character varying ,"DNA" character varying ,"DNA-II" integer )

-- DDLs for Database: toxicology --
-- public.atom --
-- Table definition
CREATE TABLE public.atom (atom_id character varying ,molecule_id character varying ,element character varying )

-- public.bond --
-- Table definition
CREATE TABLE public.bond (bond_id character varying ,molecule_id character varying ,bond_type character varying )

-- public.connected --
-- Table definition
CREATE TABLE public.connected (atom_id character varying ,atom_id2 character varying ,bond_id character varying )

-- public.molecule --
-- Table definition
CREATE TABLE public.molecule (molecule_id character varying ,label character varying )

