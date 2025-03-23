----- DELETE -----
-- Any previous test data needs to be deleted to prevent id conflicts and maintain consistent tests.

-- DELETE * FROM public."Dashboard_quicklinks" WHERE "id" > 100

DELETE FROM public."FarmAcc_farminfo" WHERE "id" > 100;
-- DELETE * FROM public."FarmAcc_filecategory" WHERE "id" > 100
-- DELETE * FROM public."FarmAcc_filerecord" WHERE "id" > 100

DELETE FROM public."Settings_internalteamsmodel" WHERE "farm_id" > 100;
-- DELETE FROM public."Settings_orgsettingsmodel" WHERE "id" > 100; -- Needs deleting?

DELETE FROM public."Tasks_task" WHERE "taskID" > 100;
-- DELETE FROM public."Tasks_step" WHERE "stepID" > 100;
-- DELETE FROM public."Tasks_label" WHERE "labelID" > 100;
DELETE FROM public."Tasks_kanbans" WHERE "kanbanID" > 100;
DELETE FROM public."Tasks_kanbancontents" WHERE "kanbanContentsID" > 100;

-- public."UserAuth_securitygroup" is static
DELETE FROM public."UserAuth_userprofile" WHERE "id" > 100;
DELETE FROM public."UserAuth_userprofile_groups" WHERE "userprofile_id" > 100;
-- DELETE * FROM public."UserAuth_userprofile_user_permissions" WHERE "id" > 100

-- public."auth_group" is static
-- public."auth_group_permissions" is static
-- public."auth_permission" is static, probably


----- Dashboard -----
-- INSERT INTO public."Dashboard_quicklinks"
-- 	("id", "quickLinkName", "link", "user_id", "icon")
-- VALUES
-- 	();


----- FarmAcc -----
INSERT INTO public."FarmAcc_farminfo"
	("id", "farm_name", "farm_street", "farm_state", "farm_postcode", "farm_bio", "farm_image")
VALUES
--	"id", "farm_name", "farm_street", "farm_state", "farm_postcode",
--		"farm_bio",
--		"farm_image"
	(101, 'Green Meadows Farm'	, '123 Sunshine Road'	, 'QLD', '4000',
		'Green Meadows Farm is nestled in the picturesque countryside of Queensland. We specialize in organic produce, cultivating a wide variety of fruits and vegetables using sustainable farming practices. Our farm is committed to promoting environmental stewardship while providing fresh, wholesome produce to our local community.',
		'images/farm_images/greenmeadowfarm.jpg'),
	(102, 'Rolling Hills Ranch'	, '456 Riverbank Avenue', 'NSW', '2000',
		'Rolling Hills Ranch is a family-owned farm located in the heart of New South Wales. Surrounded by rolling hills and lush greenery, we raise free-range livestock, including cattle, sheep, and poultry. Our commitment to animal welfare and sustainable agriculture ensures that our products are of the highest quality, providing nutritious and delicious options for our customers.',
		'images/farm_images/rollinghillsfarm.jpg'),
	(103, 'Sunset Vineyards'	, '789 Vineyard Lane'	, 'VIC', '3000',
		'Sunset Vineyards is a boutique winery situated in the beautiful countryside of Victoria. Our vineyard benefits from the unique microclimate of the region, producing award-winning wines with distinct flavors and aromas. We take pride in our hands-on approach to winemaking, from grape cultivation to bottling, ensuring that each bottle reflects the passion and dedication we have for our craft.',
		'images/farm_images/sunsetvineyards.jpg');

-- INSERT INTO public."FarmAcc_filecategory"
-- 	("id", "fileCategoryName")
-- VALUES
-- 	();

-- INSERT INTO public."FarmAcc_filerecord"
-- 	("id", "fileName", "reviewDate", "file", "fileCategory_id")
-- VALUES
-- 	();


----- Settings -----
INSERT INTO public."Settings_internalteamsmodel"
	("group_ptr_id", "teamName", "teamDescription", "active", "teamImage", "farm_id")
VALUES
--	"group_ptr_id", "teamName",
--		"teamDescription",
--		"active", "teamImage", "farm_id"
	(1, 'Harvest Crew',
		'Responsible for managing and executing the harvest activities at Green Meadows Farm.',
		true , 'images/farm_images/greenmeadowfarm.jpg'	, 101),
	(2, 'Livestock Care Team',
		'Handles the care, feeding, and health maintenance of livestock at Green Meadows Farm.', 
		true , 'images/farm_images/greenmeadowfarm.jpg'	, 101),
	(3, 'Orchard Management Team',
		'Manages the orchard operations, including planting, pruning, and harvesting of fruit trees.',
		true , 'images/farm_images/greenmeadowfarm.jpg'	, 101),
	(4, 'Poultry Production Team',
		'Handles all aspects of poultry production, including breeding, hatching, and raising chickens.',
		true , 'images/farm_images/rollinghillsfarm.jpg', 102),
	(5, 'Dairy Operations Team',
		'Manages the day-to-day operations of the dairy farm, including milking, feeding, and herd management.',
		true , 'images/farm_images/rollinghillsfarm.jpg', 102),
	(6, 'Crop Cultivation Team',
		'Responsible for planting, growing, and harvesting crops at Rolling Hills Ranch.',
		true , 'images/farm_images/rollinghillsfarm.jpg', 102),
	(7, 'Vineyard Maintenance Crew',
		'Handles the maintenance tasks required to keep the vineyard in optimal condition.',
		true , 'images/farm_images/sunsetvineyards.jpg'	, 103),
	(8, 'Winemaking Team',
		'Oversees the winemaking process from grape selection to bottling at Sunset Vineyards.',
		true , 'images/farm_images/sunsetvineyards.jpg'	, 103),
	(9, 'Vineyard Research Team',
		'Conducts research and experimentation to improve vineyard practices and grape quality.',
		true , 'images/farm_images/sunsetvineyards.jpg'	, 103);

-- INSERT INTO public."Settings_orgsettingsmodel"
-- 	("id", "timezone", "datetime_format", "temperature_label", "mass_label", "area_label", "length_label")
-- VALUES
-- 	();


----- Tasks -----
INSERT INTO public."Tasks_task"
	("taskID", "name", "description", "assignedTo_id", "timeStamp", "isCompleted", "isArchived", "isDeleted", "status", "priority", "dueDate", "expiry")
VALUES
--	"taskID", "name", "description"
-- 		"assignedTo_id", "timeStamp", "isCompleted", "isArchived", "isDeleted", "status", "priority", "dueDate", "expiry"
	(101, 'Planting Corn'						, 'Prepare and sow corn seeds in designated fields for the upcoming season.',
		102, NOW(), false, false, false, 1, 2, NOW() + INTERVAL '0' DAY, NOW() + INTERVAL '2' DAY),
	(102, 'Fertilizer Application'				, 'Apply appropriate fertilizers to enhance soil fertility and promote crop growth.',
		102, NOW(), false, false, false, 0, 0, NOW() + INTERVAL '0' DAY, NOW() + INTERVAL '2' DAY),
	(103, 'Livestock Feeding'					, 'Provide feed and water to livestock according to their dietary requirements.',
		102, NOW(), false, false, false, 2, 1, NOW() + INTERVAL '0' DAY, NOW() + INTERVAL '2' DAY),
	(104, 'Crop Irrigation'						, 'Manage irrigation schedules to ensure crops receive adequate water for optimal growth.',
		102, NOW(), false, false, false, 3, 1, NOW() + INTERVAL '0' DAY, NOW() + INTERVAL '2' DAY),
	(105, 'Weed Control'						, 'Implement weed control measures to minimize competition for nutrients and space among crops.',
		102, NOW(), true , false, false, 4, 0, NOW() + INTERVAL '0' DAY, NOW() + INTERVAL '2' DAY),
	(106, 'Harvesting Vegetables'				, 'Harvest ripe vegetables from the fields or garden for sale or consumption.',
		102, NOW(), true , false, false, 4, 1, NOW() + INTERVAL '0' DAY, NOW() + INTERVAL '2' DAY),

	(107, 'Pruning Fruit Trees'					, 'Trim and prune fruit trees to remove dead or excess branches and encourage fruit production.',
		103, NOW(), false, false, false, 0, 0, NOW() + INTERVAL '0' DAY, NOW() + INTERVAL '2' DAY),
	(108, 'Field Scouting'						, 'Regularly inspect fields for signs of pests, diseases, or other issues that may affect crop health.',
		103, NOW(), false, false, false, 0, 1, NOW() + INTERVAL '0' DAY, NOW() + INTERVAL '2' DAY),
	(109, 'Equipment Maintenance'				, 'Perform routine maintenance and repairs on farm equipment to ensure functionality.',
		104, NOW(), false, false, false, 1, 2, NOW() + INTERVAL '0' DAY, NOW() + INTERVAL '2' DAY),
	(110, 'Market Research'						, 'Conduct market research to analyze demand trends and prices for farm products.',
		104, NOW(), false, false, false, 0, 0, NOW() + INTERVAL '1' DAY, NOW() + INTERVAL '2' DAY),
--	"taskID", "name", "description"
-- 		"assignedTo_id", "timeStamp", "isCompleted", "isArchived", "isDeleted", "status", "priority", "dueDate", "expiry"
	(111, 'Livestock Health Check'				, 'Monitor the health and well-being of livestock and administer necessary treatments.',
		104, NOW(), false, false, false, 0, 0, NOW() + INTERVAL '1' DAY, NOW() + INTERVAL '2' DAY),
	(112, 'Crop Rotation Planning'				, 'Develop and implement a crop rotation plan to optimize soil fertility and minimize disease pressure.',
		105, NOW(), false, false, false, 0, 0, NOW() + INTERVAL '1' DAY, NOW() + INTERVAL '2' DAY),
	(113, 'Soil Sampling'						, 'Collect soil samples for analysis to determine nutrient levels and pH balance.',
		105, NOW(), false, false, false, 0, 0, NOW() + INTERVAL '1' DAY, NOW() + INTERVAL '2' DAY),
	(114, 'Greenhouse Management'				, 'Monitor environmental conditions in greenhouses and adjust as needed for plant growth.',
		106, NOW(), false, false, false, 0, 0, NOW() + INTERVAL '1' DAY, NOW() + INTERVAL '2' DAY),
	(115, 'Pest Management'						, 'Implement integrated pest management strategies to control pest populations while minimizing environmental impact.',
		106, NOW(), false, false, false, 0, 0, NOW() + INTERVAL '1' DAY, NOW() + INTERVAL '2' DAY),
	(116, 'Weather Monitoring'					, 'Monitor weather forecasts and conditions to make informed decisions regarding farm operations.',
		106, NOW(), false, false, false, 0, 0, NOW() + INTERVAL '1' DAY, NOW() + INTERVAL '2' DAY),
	(117, 'Seed Selection'						, 'Research and select appropriate seeds for planting based on crop type, climate, and soil conditions.',
		107, NOW(), false, false, false, 0, 0, NOW() + INTERVAL '1' DAY, NOW() + INTERVAL '2' DAY),
	(118, 'Livestock Breeding'					, 'Manage breeding programs for livestock to improve genetic traits and productivity.',
		107, NOW(), false, false, false, 0, 0, NOW() + INTERVAL '1' DAY, NOW() + INTERVAL '2' DAY),
	(119, 'Compost Production'					, 'Manage composting operations to recycle organic waste into nutrient-rich soil amendments.',
		108, NOW(), false, false, false, 0, 0, NOW() + INTERVAL '1' DAY, NOW() + INTERVAL '2' DAY),
	(120, 'Crop Harvest Planning'				, 'Plan and coordinate harvest schedules to ensure efficient and timely collection of crops.',
		108, NOW(), false, false, false, 0, 0, NOW() + INTERVAL '1' DAY, NOW() + INTERVAL '2' DAY),
--	"taskID", "name", "description"
-- 		"assignedTo_id", "timeStamp", "isCompleted", "isArchived", "isDeleted", "status", "priority", "dueDate", "expiry"
	(121, 'Crop Storage'						, 'Properly store harvested crops to maintain quality and prevent spoilage.',
		108, NOW(), false, false, false, 0, 0, NOW() + INTERVAL '1' DAY, NOW() + INTERVAL '2' DAY),
	(122, 'Irrigation System Maintenance'		, 'Inspect and maintain irrigation systems to prevent leaks and ensure efficient water distribution.',
		109, NOW(), false, false, false, 0, 0, NOW() + INTERVAL '1' DAY, NOW() + INTERVAL '2' DAY),
	(123, 'Herbicide Application'				, 'Apply herbicides as needed to control weed populations and preserve crop yields.',
		109, NOW(), false, false, false, 0, 0, NOW() + INTERVAL '1' DAY, NOW() + INTERVAL '2' DAY),
	(124, 'Livestock Grazing Management'		, 'Manage rotational grazing systems to optimize pasture health and livestock productivity.',
		110, NOW(), false, false, false, 0, 0, NOW() + INTERVAL '1' DAY, NOW() + INTERVAL '2' DAY),
	(125, 'Food Safety Compliance'				, 'Ensure compliance with food safety regulations and standards for farm products.',
		110, NOW(), false, false, false, 0, 0, NOW() + INTERVAL '1' DAY, NOW() + INTERVAL '2' DAY),
	(126, 'Field Preparation'					, 'Prepare fields for planting by tilling, leveling, and removing debris.',
		110, NOW(), false, false, false, 0, 0, NOW() + INTERVAL '1' DAY, NOW() + INTERVAL '2' DAY),
	(127, 'Disease Management'					, 'Implement disease management strategies to prevent and control outbreaks in crops and livestock.',
		111, NOW(), false, false, false, 0, 0, NOW() + INTERVAL '1' DAY, NOW() + INTERVAL '2' DAY),
	(128, 'Record Keeping'						, 'Maintain accurate records of farm activities, expenses, and yields for financial and regulatory purposes.',
		111, NOW(), false, false, false, 0, 0, NOW() + INTERVAL '1' DAY, NOW() + INTERVAL '2' DAY),

	(129, 'Employee Training'					, 'Provide training and supervision to farm workers to ensure safe and efficient operation of equipment and tasks.',
		101, NOW(), false, false, false, 0, 0, NOW() + INTERVAL '1' DAY, NOW() + INTERVAL '2' DAY),
	(130, 'Farm Infrastructure Maintenance'		, 'Inspect and maintain farm buildings, fences, and other infrastructure to ensure safety and functionality.',
		101, NOW(), false, false, false, 0, 0, NOW() + INTERVAL '1' DAY, NOW() + INTERVAL '2' DAY),
--	"taskID", "name", "description"
-- 		"assignedTo_id", "timeStamp", "isCompleted", "isArchived", "isDeleted", "status", "priority", "dueDate", "expiry"
	(131, 'Cover Crop Planting'					, 'Plant cover crops to improve soil health, prevent erosion, and suppress weed growth during fallow periods.',
		101, NOW(), false, false, false, 0, 0, NOW() + INTERVAL '1' DAY, NOW() + INTERVAL '2' DAY),
	(132, 'Poultry Egg Collection'				, 'Collect eggs from poultry houses and ensure proper storage and handling.',
		101, NOW(), false, false, false, 0, 0, NOW() + INTERVAL '1' DAY, NOW() + INTERVAL '2' DAY),
	(133, 'Livestock Vaccination'				, 'Administer vaccinations to livestock according to recommended schedules to prevent disease.',
		101, NOW(), false, false, false, 0, 0, NOW() + INTERVAL '1' DAY, NOW() + INTERVAL '2' DAY),
	(134, 'Crop Pollination Management'			, 'Manage pollination activities for crops that require insect pollinators or other methods.',
		101, NOW(), false, false, false, 1, 0, NOW() + INTERVAL '1' DAY, NOW() + INTERVAL '2' DAY),
	(135, 'Food Processing'						, 'Process farm products such as fruits, vegetables, and meat for sale or distribution.',
		101, NOW(), false, false, false, 2, 0, NOW() + INTERVAL '1' DAY, NOW() + INTERVAL '2' DAY),
	(136, 'Organic Certification Compliance'	, 'Maintain compliance with organic farming standards and regulations for certified organic products.',
		101, NOW(), false, false, false, 2, 0, NOW() + INTERVAL '1' DAY, NOW() + INTERVAL '2' DAY),
	(137, 'Farmers Market Participation'		, 'Prepare and transport farm products for sale at farmers markets or other direct-to-consumer outlets.',
		101, NOW(), false, false, false, 2, 0, NOW() + INTERVAL '1' DAY, NOW() + INTERVAL '2' DAY),
	(138, 'Community Engagement'				, 'Engage with local community members through educational events, tours, or volunteer opportunities.',
		101, NOW(), false, false, false, 2, 0, NOW() + INTERVAL '1' DAY, NOW() + INTERVAL '2' DAY),
	(139, 'Wildlife Habitat Management'			, 'Manage wildlife habitats on the farm to promote biodiversity and ecosystem health.',
		101, NOW(), false, false, false, 3, 0, NOW() + INTERVAL '1' DAY, NOW() + INTERVAL '2' DAY),
	(140, 'Emergency Preparedness'				, 'Develop and implement emergency response plans for natural disasters or other emergencies.',
		101, NOW(), false, false, false, 4, 0, NOW() + INTERVAL '1' DAY, NOW() + INTERVAL '2' DAY),
--	"taskID", "name", "description"
-- 		"assignedTo_id", "timeStamp", "isCompleted", "isArchived", "isDeleted", "status", "priority", "dueDate", "expiry"
	(141, 'Farm Budgeting'						, 'Develop and manage budgets for farm operations, including expenses and income projections.',
		101, NOW(), false, false, false, 0, 0, NOW() + INTERVAL '1' DAY, NOW() + INTERVAL '2' DAY),
	(142, 'Soil Erosion Control'				, 'Implement erosion control measures such as contour plowing, terracing, or cover cropping to prevent soil loss.',
		101, NOW(), false, false, false, 1, 0, NOW() + INTERVAL '1' DAY, NOW() + INTERVAL '2' DAY),
	(143, 'Livestock Slaughter and Processing'	, 'Humanely slaughter and process livestock for sale or consumption according to regulations.',
		101, NOW(), false, false, false, 1, 0, NOW() + INTERVAL '1' DAY, NOW() + INTERVAL '2' DAY),
	(144, 'Food Packaging and Labeling'			, 'Package and label farm products for retail sale, including compliance with labeling requirements.',
		101, NOW(), false, false, false, 1, 0, NOW() + INTERVAL '1' DAY, NOW() + INTERVAL '2' DAY),
	(145, 'Farmers Association Membership'		, 'Participate in local or regional farmers associations for networking and advocacy.',
		101, NOW(), false, false, false, 1, 0, NOW() + INTERVAL '1' DAY, NOW() + INTERVAL '2' DAY),
	(146, 'Agroforestry Planning'				, 'Integrate tree crops into farming systems to provide additional income streams and environmental benefits.',
		101, NOW(), false, false, false, 2, 0, NOW() + INTERVAL '1' DAY, NOW() + INTERVAL '2' DAY),
	(147, 'Water Conservation Practices'		, 'Implement water conservation practices such as drip irrigation or rainwater harvesting to reduce water usage.',
		101, NOW(), false, false, false, 2, 0, NOW() + INTERVAL '1' DAY, NOW() + INTERVAL '2' DAY),
	(148, 'Farm Tourism Development'			, 'Develop agritourism opportunities such as farm tours, educational programs, or farm stays.',
		101, NOW(), false, false, false, 3, 0, NOW() + INTERVAL '1' DAY, NOW() + INTERVAL '2' DAY),
	(149, 'Renewable Energy Integration'		, 'Integrate renewable energy sources such as solar panels or wind turbines into farm operations.',
		101, NOW(), false, false, false, 3, 0, NOW() + INTERVAL '1' DAY, NOW() + INTERVAL '2' DAY),
	(150, 'Climate Change Adaptation Strategies', 'Develop and implement strategies to adapt farm operations to changing climate conditions, such as drought-resistant crop varieties or water-saving technologies.',
		101, NOW(), false, false, false, 4, 0, NOW() + INTERVAL '1' DAY, NOW() + INTERVAL '2' DAY);
--	"taskID", "name", "description"
-- 		"assignedTo_id", "timeStamp", "isCompleted", "isArchived", "isDeleted", "status", "priority", "dueDate", "expiry"

-- INSERT INTO public."Tasks_step"
-- 	("stepID", "order", "completed", "description", "parentTask_id")
-- VALUES
-- 	();

-- INSERT INTO public."Tasks_label"
-- 	("labelID", "name", "colour", "kanban", "parentLabel_id")
-- VALUES
-- 	();

INSERT INTO public."Tasks_kanbans"
	("kanbanID", "name", "parentFarm_id")
VALUES
	(101, 'Harvest Crew'       , 101),
	(102, 'Livestock Care Team', 101);

INSERT INTO public."Tasks_kanbancontents"
	("kanbanContentsID", "order", "kanbanID_id", "taskID_id")
VALUES
-- Board 1
	(101, 0, 101, 131),
	(102, 1, 101, 132),
	(103, 2, 101, 133),
	(104, 0, 101, 134),
	(105, 0, 101, 135),
	(106, 1, 101, 136),
	(107, 2, 101, 137),
	(108, 3, 101, 138),
	(109, 0, 101, 139),
	(110, 0, 101, 140),
-- Board 2
	(111, 0, 102, 141),
	(112, 0, 102, 142),
	(113, 1, 102, 143),
	(114, 2, 102, 144),
	(115, 3, 102, 145),
	(116, 0, 102, 146),
	(117, 1, 102, 147),
	(118, 0, 102, 148),
	(119, 1, 102, 149),
	(120, 0, 102, 150);


----- UserAuth -----
-- INSERT INTO public."UserAuth_securitygroup"
-- 	("group_ptr_id")
-- VALUES
-- 	(1), (2), (3), (4), (5), (6), (7), (8), (9);

INSERT INTO public."UserAuth_userprofile"
	("id", "password", "last_login", "is_superuser", "username", "first_name", "last_name", "email", "is_staff", "is_active", "date_joined", "firstName", "lastName", "jobTitle", "workingLocation", "role", "phoneNumber", "farm_id")
VALUES
--	"id", "password", "last_login",
--		"is_superuser", "username", "first_name", "last_name", "email", "is_staff", "is_active",
--		"date_joined", "firstName", "lastName", "jobTitle", "workingLocation", "role", "phoneNumber", "farm_id"
	-- john.smith, G#p9Xz3@
	(101, 'pbkdf2_sha256$720000$htzWZhuAWM5CmHkp5P85jk$VpYkPB1hLxWHD8LI2eJN5EVj6ITP7kIQ1i0Q2wOS/EA=', '2024-05-27 21:56:53.413704+10',
		false, 'john.smith'		, 'John'	, 'Smith'	, 'john.smith@greenmeadowsfarm.com'			, false, true ,
		'2024-05-27 21:56:20.314859+10', NULL, NULL, 'Farm Manager'				, 'On Site', 'Manager'		, '+61 123 456 789', 101),
	-- sarah.martinez, W8d$Jr4@
	(102, 'pbkdf2_sha256$720000$uMwo2BqMd196c9G1sBd1G8$3qldjuSTjxOxgCgXu4wXokqPeA3BNOeAJ5B9hSqaUFU=', NULL,
		false, 'sarah.martinez'	, 'Sarah'	, 'Martinez', 'sarah.martinez@greenmeadowsfarm.com'		, false, true ,
		'2024-05-27 22:06:48.378544+10', NULL, NULL, 'Agricultural Technician'	, 'On Site', 'Technician'	, '+61 456 789 012', 101),
	-- matthew.white, H7z@Gp5!
	(103, 'pbkdf2_sha256$720000$ThV9I28WJNKPn2QDCySiFV$U7fSZN4CAlZ6Ay7DyBDWV86zAex05oM7pvbideHZG7k=', NULL, 
		false, 'matthew.white'	, 'Matthew'	, 'White'	, 'matthew.white@greenmeadowsfarm.com'		, false, true ,
		'2024-05-27 22:08:00.252852+10', NULL, NULL, 'Crop Manager'				, 'On Site', 'Manager'		, '+61 789 012 345', 101),
	-- daniel.garcia, S3g@Yt8!
	(104, 'pbkdf2_sha256$720000$ln0cLdz2l5JRHKGpV6kw6M$pgd7vA4G+O7Gwnv8l8UIxe1+eYz37UPaOZC/15lSWmQ=', NULL,
		false, 'daniel.garcia'	, 'Daniel'	, 'Garcia'	, 'daniel.garcia@greenmeadowsfarm.com'		, false, false,
		'2024-05-27 22:09:14.36279+10' , NULL, NULL, 'Orchardist'				, 'On Site', 'Specialist'	, '+61 901 234 567', 101),
	-- olivia.jones, P3r@Lm6#
	(105, 'pbkdf2_sha256$720000$4SFgOhQBaAcPD7hm12GRLM$wyeqiCN87IvesmuVouSA0VFoKZnaXmHc5vQsHm0+djU=', NULL,
		false, 'olivia.jones'	, 'Olivia'	, 'Jones'	, 'olivia.jones@greenmeadowsfarm.com'		, false, true ,
		'2024-05-27 22:10:33.84915+10' , NULL, NULL, 'Dairy Supervisor'			, 'On Site', 'Supervisor'	, '+61 234 567 890', 101),
--	"id", "password", "last_login",
--		"is_superuser", "username", "first_name", "last_name", "email", "is_staff", "is_active",
--		"date_joined", "firstName", "lastName", "jobTitle", "workingLocation", "role", "phoneNumber", "farm_id"
	-- william.smith, M8b!Qz3@
	(106, 'pbkdf2_sha256$720000$AxSQW8vU8oP7DvBdD4Nlhd$yxYeAIbEBFTwo3vKUbM99EC6TD9XQTZY28/TLyhwgTU=', NULL,
		false, 'william.smith'	, 'William'	, 'Smith'	, 'william.smith@greenmeadowsfarm.com'		, false, false,
		'2024-05-27 22:11:53.630949+10', NULL, NULL, 'Farmhand'					, 'On site', 'Farmhand'		, '+61 345 678 901', 101),
	-- emma.davis, N9c$Wx2!
	(107, 'pbkdf2_sha256$720000$1togAub6fqYtv61iQ7BVNz$N5ITDeOvRYDNZD7GNsc58HHX26s9kglybz8/8XoOLpM=', NULL, 
		false, 'emma.davis'		, 'Emma'	, 'Davis'	, 'emma.davis@greenmeadowsfarm.com'			, false, true ,
		'2024-05-27 22:12:53.346354+10', NULL, NULL, 'Specialist'				, 'On site', 'Specialist'	, '+61 456 789 012', 101),
	-- jack.miller, F5g#Qw9!
	(108, 'pbkdf2_sha256$720000$E1BT49do994dGyMPaHNvU7$EoV4i7wc3+3RmFilVttJ4v7hKVVvmn17erOzUWYB8oo=', NULL,
		false, 'jack.miller'	, 'Jack'	, 'Miller'	, 'jack.miller@greenmeadowsfarm.com'		, false, false,
		'2024-05-27 22:14:39.661002+10', NULL, NULL, 'Field Worker'				, 'On site', 'Worker'		, '+61 456 789 012', 101),
	-- sophie.wilson, L4p@Rt8!
	(109, 'pbkdf2_sha256$720000$FRSIsPZCzuJCzKnfYgP3lL$3lQCErj2TN0GDa2qIo6lRSAz/rSlwMLyZDiIkZ4DXrs=', NULL,
		false, 'sophie.wilson'	, 'Sophie'	, 'Wilson'	, 'sophie.wilson@greenmeadowsfarm.com'		, false, true ,
		'2024-05-27 22:16:09.119923+10', NULL, NULL, 'Garden Supervisor'		, 'On site', 'Supervisor'	, '+61 678 901 234', 101),
	-- lucas.brown, T7v@Np2#
	(110, 'pbkdf2_sha256$720000$KmVmnlWcYRY3D5bbJAcpbj$z4Zy+ONUupL0eGlF4Mg5gkqJ9PUUjzQWlIvZlKsp+qg=', NULL,
		false, 'lucas.brown'	, 'Lucas'	, 'Brown'	, 'lucas.brown@greenmeadowsfarm.com'		, false, false,
		'2024-05-27 22:17:29.070465+10', NULL, NULL, 'Harvest Manager'			, 'On site', 'Manager'		, '+61 789 012 345', 101),
--	"id", "password", "last_login",
--		"is_superuser", "username", "first_name", "last_name", "email", "is_staff", "is_active",
--		"date_joined", "firstName", "lastName", "jobTitle", "workingLocation", "role", "phoneNumber", "farm_id"
	--T@6bYw8!, emily.johnson
	(111, 'pbkdf2_sha256$720000$fGIYrUEAX9vXCzKXLtzQHQ$hYzan1tp0TD0FrwByq9q5JcDWDAG3/rs9xtR+NEZoWM=', NULL,
		false, 'emily.johnson'	, 'Emily'	, 'Johnson'	, 'emily.johnson@rollinghillsranch.com'		, false, true ,
		'2024-05-27 22:49:21.24416+10' , NULL, NULL, 'Livestock Supervisor'		, 'On Site', 'Supervisor'	, '+61 234 567 890', 101);

INSERT INTO public."UserAuth_userprofile_groups"
	("id", "userprofile_id", "group_id")
VALUES -- Need to get proper group_id values, I resolved conflicts by choosing a random value
	(101, 101, 5),
	(102, 102, 1),
	(103, 103, 1),
	(104, 104, 1),
	(105, 104, 9),
	(106, 106, 9),
	(107, 107, 1),
	(108, 108, 1),
	(109, 108, 8),
	(110, 109, 1),
	(111, 110, 1),
	(112, 110, 8),
	(113, 111, 1),
	(114, 111, 4);

-- INSERT INTO public."UserAuth_userprofile_user_permissions"
-- 	("id", "userprofile_id", "permission_id")
-- VALUES
-- 	();


----- auth -----
-- INSERT INTO public."auth_group"
-- 	("id", "name")
-- VALUES
-- 	( 1, 'Farm Employee'			),
-- 	( 2, 'Inventory Manager'		),
-- 	( 3, 'Farm Manager'				),
-- 	( 4, 'Team Leader'				),
-- 	( 5, 'Farm Owner'				),
-- 	( 6, 'Fleet Manager'			),
-- 	( 7, 'Farm Operations Manager'	),
-- 	( 8, 'Storage Manager'			),
-- 	( 9, 'Financial Controller'		),
-- 	(10, ''							), -- Meant to be Harvester Crew
-- 	(18, 'Livestock Care Team'		),
-- 	(19, 'Orchard Management Team'	);

-- INSERT INTO public."auth_group_permissions"
-- 	("id", "group_id", "permission_id")
-- VALUES
-- 	(1, 5, 29);

-- INSERT INTO public."auth_permission"
-- 	("id", "name", "content_type_id", "codename")
-- VALUES
-- 	();
