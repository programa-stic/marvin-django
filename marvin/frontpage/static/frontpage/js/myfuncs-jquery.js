// Copyright (c) 2015-2016, Fundacion Dr. Manuel Sadosky
// All rights reserved.

// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are met:

// 1. Redistributions of source code must retain the above copyright notice, this
// list of conditions and the following disclaimer.

// 2. Redistributions in binary form must reproduce the above copyright notice,
// this list of conditions and the following disclaimer in the documentation
// and/or other materials provided with the distribution.

// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
// AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
// IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
// DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
// FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
// DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
// SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
// CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
// OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
// OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

$(document).ready(function() {

	// JQuery code to be added in here.
	$( ".permission" ).toggle();
	$( ".activity" ).toggle();
	$( ".receiver" ).toggle();
	$( ".service" ).toggle();
	$( ".provider" ).toggle();
	$( ".packages" ).toggle();
	$( ".vulnerabilities" ).toggle();



	$( "#perms-btn" ).click(function(event) {
		$( ".permission" ).toggle(400);
	})

	$( "#acts-btn" ).click(function(event) {
		$( ".activity" ).toggle(400);
	})
	$( "#recvs-btn" ).click(function(event) {
		$( ".receiver" ).toggle(400);
	})

	$( "#servs-btn" ).click(function(event) {
		$( ".service" ).toggle(400);
	})

	$( "#vulns-btn" ).click(function(event) {
		$( ".vulnerabilities" ).toggle(400);
	})

	$( "#provs-btn" ).click(function(event) {
		$( ".provider" ).toggle(400);
	})

	$( "#pkgs-btn" ).click(function(event) {
		$( ".packages" ).toggle(400);
	})



	
});
