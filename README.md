ASC 606 and IFRS 15 are accounting standards that I particularly admire for their conservative yet equitable nature. While some companies find adopting ASC 606 and implementing proper revenue recognition to be a straightforward process, others face challenges due to the complexity of their major contracts, extensive contract modifications, and variable consideration and material rights issues. Many of these companies have been relying on Excel or Google Sheets to manage their revenue recognition models, leading to inevitable failures and the accumulation of manual errors and mistakes that often go unnoticed.

To address this problem, numerous cloud-based revenue recognition system providers are now available. While I encourage everyone to research and explore these solutions, it's worth noting that cloud solutions may not be suitable for businesses lacking compatible finance infrastructure (modern CPQ, billing, and ERP QTC systems and processes) or those with concerns about data privacy and regulation compliance. Additionally, cloud solutions may lack the necessary flexibility to accommodate tailored accounting treatments required by specific industries.

Hence, I developed eRev, a pure Python packaged revenue recognition system comprising only 13 buttons to handle almost all revenue recognition needs. Recognizing that accountants may not always have access to high-end laptops, I worked to ensure that the system is lightweight and can run efficiently on various Windows laptops available on the market today.

Here are some highlights of the system's overall operations:

1.    It is very affordable, with the full ASC 606 & IFRS 15 functions free of charge under the Free-Tier Program. See the Free-Tier Program agreement and the flat pricing for the premium functions on this web page below.

2.    It is safe. The system will enable Window's built-in EFS (explained here: https://learn.microsoft.com/en-us/windows/win32/fileio/file-encryption) to protect your local ASC606 database file. Unlike Excel, you don't need to enter a password to access your data. As long as you can successfully log in to your Windows account, the database is made available to you (your admin can also access the database, which is the design of EFS). Hackers, on the other hand, cannot access your database without your private key, even if somehow they manage to steal the database file (this is not an absolute promise because nothing is perfectly safe).

3.    It is limitless, fast, and easy to share with integrity. SQLite is used as our ASC606 database. It is a single file that can be easily transferred to anyone in case of employee turnover (which always occurs more than we want). And of course, the encryption needs to be removed manually before sharing, as no one else will be able to access the database you created (with the exception of your IT administrator as explained in #2 above). SQLite technically has a record limit, but in the field of revenue accounting, we don't need to worry about this unless you have millions of contracts you want to run through the system daily. Even then, eRev is built so that you can easily archive your old database and start a new one with the latest revenue accounting history. I chose SQLite mainly because it is super lightweight, super-fast, and reliable, with all changes and queries being atomic, consistent, isolated, and durable (ACID).

4.    I always strive to build the best solution for practical revenue accounting use. Here are the 5 buttons for the database operations:

a.    Backup – you can easily back up the single file SQLite ASC606 database anytime you want, often in milliseconds if your laptop is as fast as mine. Save the backup periodically to a cloud drive so you can restore it in case of a disaster on your local machine.

b.    Restore – you can easily restore your latest backup by overriding your current version with just 1 click. The reason I built this? This can serve as your UNDO button, just like in Excel and Google Sheets!

c.    Reset – many of you will use the system to simply run one-time allocation for deals in negotiation or different revenue scenario analyses you want to compose. The reset button can give you a clean start anytime you wish.

d.    Append from Another – if your revenue accounting colleagues quit accounting and you need to take care of their contracts, use this feature to take over their databases.

e.    Purge Contract – if you have any bad contracts in the database, you can use this function to purge those records.

5.    Because SQLite is arguably the most popular database in the world, your business intelligence integration requirement is already taken care of. You can easily connect your ASC606 database to PowerBI, Tableau, Alteryx, or any other popular or sophisticated data warehouse solutions you may be using. And you don't need to be a data scientist to figure out such integration.

6.    Built-in real-time tracking: every time you make a change to your contracts, whether it's a billing, a delivery, or a modification event, the system logs your actions with a timestamp so you can easily trace your activities afterward to see what you have done.

What about revenue accounting?

I will make a bold statement: the system is so intuitive that any revenue operations accountant can learn to conduct revenue recognition using eRev in under 1 hour.

And please don't confuse the simplicity of learning the system with the complexity of eRev's revenue accounting functionality – I would be deeply offended. eRev offers some of the most sophisticated revenue accounting treatments in the market because it is built by a revenue accountant (myself 😊).

Here's how it works:

The system uses 4 Excel templates to make everything work:

1 template for SSP upload, and you can muster multiple versions of SSPs all together in one file.

1 template for contract setup, and you can assign any version of SSP to any POB at your will.

1 template for delivery and billing.

1 template for contract mods (works for both prospective contract mods and retrospective contract mods).

6 buttons correspond to the templates above (contract mods have three buttons, prospective contract mod, retrospective contract mod and POB specific variable consideration).

eRev as a complete revenue system, can perform transaction price allocation based on SSPs, revenue recognition based on deliveries and billings, and modifications. Using Excel uploads, SQLite, and Python-based functions collectively, eRev offers a ton of special flexibility (compared to most cloud-based solutions), so you can:

1.    Set different SSP methodologies at whichever product level you prefer. For contract mods, you have complete control to tell the system to use whichever version of SSPs for whichever modifications at your own will at the POB level.

2.    You can set a different revenue account for each product easily in the SSP upload template and create as many ASC 606 stratifications as you see fit.

3.    In setting up POBs, again, you have complete control to set deferred revenue accounts and unbilled A/R (contract assets) accounts differently based on the different business entities you want to assign POBs. Cross-subsidiary contract allocation is no problem at all.

4.    And of course, eRev can accommodate $0 POBs, returns (negative quantity and negative billing), material rights, and variable consideration (negative transaction price).

5.    eRev can support both distinct POBs and non-distinct POBs. Kindly see what eRev can do with non-distinct POBs in #7 below.

6. eRev has numerous built-in validation rules, such as user-input validations over dates, contents, and formats, automatic validations of delivery and billing inputs (so you don't deliver or bill more than your contract stipulates), and many contract modification integrity checks. These rules relieve concerns of human error when pulling the data together if not directly system-generated. 

7.    eRev doesn't freeze periods and doesn't take shortcuts or accounting conventions in deeming all deliveries or billings or contract mods happening at a specified time. You have complete freedom in using actual billing, delivery, and contract mods dates you like.

8.    For contract modifications:

Built-in prospective contract modification and retrospective contract modification functionalities are available without extra fees (these are essentials in revenue accounting and shouldn't be considered add-ons).

eRev supports cumulative catchup calculation for all POBs in a retrospective contract modification.

eRev supports cumulative catchup calculation for non-distinct POBs in a prospective contract modification (many revenue accountants don't even know why this is needed, but it is).

eRev will support cumulative catchup disclosure in any contract period you choose.

eRev's contract modifications are done in line with the existing POBs, meaning you can track the lifecycle of each POB continuously in its own line without combining the extra contract mod lines that other similar ASC 606 software will create.

9.    For built-in reporting and journal entry features, there are three power buttons:

Revenue Journal Entries: simply enter a date range, and all revenue journal entries related to the existing contracts for activities in such a period will be generated in a pop-up window along with an automatically saved Excel report in the folder. Those journal entries have no complicated back-and-forth movement of credits and debits during the period (unlike many alternative Rev Rec solutions that create enormous journal entries for every activity during the period without giving a solid journal entry summary of what actually happened in accounting). The journal entries provided can be easily understood by all revenue accountants – there are a maximum of three sets of accounts used: deferred revenue, unbilled A/R (contract assets), and revenue accounts, all summarized in the period you choose. Also, note that some companies prefer to post adjustment journal entries for ASC606 (posting delta because the ERP system has already recorded pre-ASC606 revenue); eRev can also be easily configured to post ASC606 adjustments instead of entire revenue recognition journal entries.

Contract History: simply enter a date range, and all relevant contract activities will be pulled out for your review in a popup window along with an automatically saved Excel report in the folder. Each delivery & billing, and contract mod will create a different version record for a specific contract, so you can easily compare the differences within any period. The layout is nicely put together vertically, so you can add some easy subtraction formulas in Excel to see the version differences. 

Latest Contract: Do you want to quickly review the relevant contract statuses for the most recent version in your database? Clicking this button will pull out all contracts in their latest version from your ASC 606 Database.

10.    Forecast requirement? Simply copy the system to another folder and use forecast deliveries and billings to see the future forecast revenue and billing impacts without interfering with the current ASC 606 revenue recognition. Need to refresh forecast deliveries and billings periodically? Simply update your templates, reset the database (or start with the latest backup for the actuals), and re-run the events.
