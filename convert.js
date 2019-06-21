#!/usr/bin/env node
// Converts a accounts.txt to a accounts.cg.json
// it's recommended to use accounts without steamguard
// email probably doesn't match, to manually add your email (username:pass:email) you can simply
// access i.split(":")[2] and set the email field to it.
// NOTE: this needs node.js, use `npm install` to install all dependencies automatically needed before running it.
var fs = require('fs');

// Load accounts
var accounts = JSON.parse('{ "array": [], "used": 0 }');

// Temporary storage
var accounts_str = [];

// Remove \n\n by replacing it with \n
var array = fs.readFileSync('accounts.txt').toString().replace(/\n\n/g, '\n').split("\n");
array.pop();
for (i in array) {
	accounts_str.push(array[i]);
}
// Keep track of processed accs and their respective database indexes
var processed_accs = 0;
var db_idx = 0;

// Loop accs and convert to proper format
accounts_str.forEach(function (i, idx, arr) {
	var json = JSON.parse('{"login": "","password": "","email": "@inboxkitten.com","community": true,"privacy":{"profile": 3,"comments": 3,"inventory": 3,"gameDetails": 3},"avatar": "https://i.imgur.com/avatar.png","summary": "summary","username": "","created": 1533672324,"steamID": "1234567891234567"}');
	json.login = i.split(":")[0];
	json.username = json.login;
	json.password = i.split(":")[1].replace(/(\r\n|\n|\r)/gm, "");
	json.email = json.login.toLowerCase() + "@inboxkitten.com";
	accounts['array'].push(json);
	processed_accs++;
	if (processed_accs >= 1000) {
		processed_accs = 0;
		fs.writeFileSync(`accounts${db_idx}.cg.json`, JSON.stringify(accounts), "utf8");
		db_idx++;
		accounts = JSON.parse('{ "array": [], "used": 0 }');
	}
});
// Write last few accs
if (processed_accs)
	fs.writeFileSync(`accounts${db_idx}.cg.json`, JSON.stringify(accounts), "utf8");
