---
id: msg_DhviSV3XUUWWFgEXVyFoXyvCrq75NFoFc7y5oYkobptJ
kind: 1010
account_id: email_no-reply_fathom_video
created_at: 1764273780000
imported_at: 1766105319786
author_name: Fathom
title: Recap of your meeting with Jeff Emmett
thread_id: email_aae9455d38d3
platform: email
platform_id: <6928ae73f34eb_11d164735a6@fathom-sidekiq-default-2-7b94566776-vlfhv.mail>
tags: [["subject","Recap of your meeting with Jeff Emmett"],["folder","INBOX"]]
---

Meeting Purpose Sync on Folk.js progress, new hardware partnerships, and funding
opportunities. Key Takeaways - New Funding Source: ZKN, a Zero Knowledge
hardware company, will provide flow funding for Folk.js development, starting
with a few thousand dollars per month. - KeyHive Integration: Integrating
KeyHive (from Ink & Switch) will enable end-to-end encrypted CRDTs, making sync
orders of magnitude faster and enabling "smart contract analogs" on CRDTs. -
WebGPU Visualizations: New WebGPU shaders (e.g., Radiance Cascade) are being
explored to create interactive, semantic visualizations of data relationships. -
"Information Substrate" Model: A new model is being explored where protocols are
"material" that users manipulate with "instruments" (tools), breaking free from
rigid application silos. Topics ZKN Hardware & Funding - ZKN is building secure,
open-source Zero Knowledge hardware (ZKNs) that will be the foundation for a new
"alternate" network. - Device Specs: Raspberry Pi 5-based, with M2 storage,
designed for secure local compute and data sovereignty. - Network Tiers: - Fog
Computing: Home-based ZKN nodes. - Mist Computing: Mobile clients. - Funding
Commitment: ZKN will provide flow funding to support Folk.js development,
recognizing its value for building on the ZKN platform. KeyHive & CRDT-Based
Contracts - KeyHive, from Ink & Switch, enables end-to-end encryption for
AutoMerge CRDTs. - KeyHive Benefits: - Performance: Sync is orders of magnitude
faster. - Architecture: Sync servers become stateless, cheap "black boxes." -
Permissions: Uses a capabilities-based model (like a ticket) for granular, local
authorization. - "Smart Contract Analogs": KeyHive's capabilities model allows
for building contract-like logic (e.g., anonymous polls, access control)
directly on CRDTs, bypassing traditional blockchain overhead. WebGPU
Visualizations - New WebGPU shaders are being explored to create semantic
visualizations of data relationships. - Demos: - Signed Distance Fields (SDFs):
Mapping DOM nodes to SDFs for interactive morphing. - Radiance Cascade: Elements
emit color "radiance" that blends on proximity (e.g., red + blue → purple),
visualizing emergent properties. - Future Use Case: Modeling liquid flows and
pipes to visualize funding streams. "Information Substrate" Model - A new model
is being explored to break free from rigid application silos. - Problem:
Protocols (e.g., Bluesky's ATProto) support features (e.g., rich text) that
official apps don't, forcing users into siloed, copy-paste workflows. -
Solution: Treat protocols as "material" that users manipulate with "instruments"
(tools), allowing for flexible, user-defined workflows. Threshold-Based Flow
Funding (TBFF) Demo - Sean built a TBFF demo in Folk.js using propagators to
model funding streams. - TBFF Logic: - Users set a min_threshold and
max_threshold. - Funds received up to min_threshold are kept. - Funds between
min_threshold and max_threshold are split between the recipient and their "flow
forward" contacts. - Funds above max_threshold are entirely flowed forward. Next
Steps - Jeff: Draft a proposal for the ZKN flow funding sub-DAO. - Jeff: Connect
the Folk.js team with ZKN once their ZKVM is available. - Orion: Continue
KeyHive integration with Folk.js and explore CRDT-based contract analogs. -
Chris: Continue exploring the "information substrate" model. - All: Use the TBFF
demo to dogfood the flow funding concept.

FATHOM
[https://storage.googleapis.com/fathom-static-web-assets/courier/mailers/post-meeting/fathom-logo-black-2025.png]
https://fathom.video/?utm_campaign=postmeetingsummary&utm_content=header&utm_medium=email
Get your own FREE AI Meeting Assistant
[https://fathom.video/invite/uZP-Uw?utm_medium=email&utm_campaign=postmeetingsummary&utm_content=header_ad]
#1 rated on G2, 5/5, 5000+ reviews
[https://storage.googleapis.com/fathom-static-web-assets/courier/mailers/post-meeting/g2-rating.png]
https://www.g2.com/products/fathom-2021-09-22/reviews

Meeting with Jeff Emmett

zkFolkJS myceliation November 27, 2025  •  60 mins  •  View Meeting
[https://fathom.video/share/o52tuXVsCJxmz3yVBs8aieEWRKxDPuba?tab=summary&utm_campaign=postmeetingsummary&utm_content=view_recording_link&utm_medium=email]
or Ask Fathom
[https://fathom.video/share/o52tuXVsCJxmz3yVBs8aieEWRKxDPuba?tab=ask_fathom&utm_campaign=postmeetingsummary&utm_content=ask_fathom&utm_medium=email]

Action Items ✨

[https://storage.googleapis.com/fathom-static-web-assets/courier/mailers/post-meeting/ico-05.png]

Set up torrent request for
movies.jeffemmett.com[https://storage.googleapis.com/fathom-static-web-assets/courier/mailers/post-meeting/ico-play-black.png]
[https://fathom.video/share/o52tuXVsCJxmz3yVBs8aieEWRKxDPuba?tab=summary&timestamp=2161.9999&utm_campaign=postmeetingsummary&utm_content=action_item&utm_medium=email]
Jeff Emmett

Meeting Summary ✨


MEETING PURPOSE

Sync on Folk.js progress, new hardware partnerships, and funding opportunities.


KEY TAKEAWAYS

 * New Funding Source: ZKN, a Zero Knowledge hardware company, will provide flow
   funding for Folk.js development, starting with a few thousand dollars per
   month.[https://storage.googleapis.com/fathom-static-web-assets/courier/mailers/post-meeting/ico-play-black.png]
   [https://fathom.video/share/o52tuXVsCJxmz3yVBs8aieEWRKxDPuba?tab=summary&timestamp=1390.0&utm_campaign=postmeetingsummary&utm_content=summary_item&utm_medium=email]

 * KeyHive Integration: Integrating KeyHive (from Ink & Switch) will enable
   end-to-end encrypted CRDTs, making sync orders of magnitude faster and
   enabling "smart contract analogs" on
   CRDTs.[https://storage.googleapis.com/fathom-static-web-assets/courier/mailers/post-meeting/ico-play-black.png]
   [https://fathom.video/share/o52tuXVsCJxmz3yVBs8aieEWRKxDPuba?tab=summary&timestamp=1625.0&utm_campaign=postmeetingsummary&utm_content=summary_item&utm_medium=email]

 * WebGPU Visualizations: New WebGPU shaders (e.g., Radiance Cascade) are being
   explored to create interactive, semantic visualizations of data
   relationships.[https://storage.googleapis.com/fathom-static-web-assets/courier/mailers/post-meeting/ico-play-black.png]
   [https://fathom.video/share/o52tuXVsCJxmz3yVBs8aieEWRKxDPuba?tab=summary&timestamp=594.0&utm_campaign=postmeetingsummary&utm_content=summary_item&utm_medium=email]

 * "Information Substrate" Model: A new model is being explored where protocols
   are "material" that users manipulate with "instruments" (tools), breaking
   free from rigid application
   silos.[https://storage.googleapis.com/fathom-static-web-assets/courier/mailers/post-meeting/ico-play-black.png]
   [https://fathom.video/share/o52tuXVsCJxmz3yVBs8aieEWRKxDPuba?tab=summary&timestamp=744.0&utm_campaign=postmeetingsummary&utm_content=summary_item&utm_medium=email]


TOPICS


ZKN HARDWARE & FUNDING

 * ZKN is building secure, open-source Zero Knowledge hardware (ZKNs) that will
   be the foundation for a new "alternate"
   network.[https://storage.googleapis.com/fathom-static-web-assets/courier/mailers/post-meeting/ico-play-black.png]
   [https://fathom.video/share/o52tuXVsCJxmz3yVBs8aieEWRKxDPuba?tab=summary&timestamp=1270.0&utm_campaign=postmeetingsummary&utm_content=summary_item&utm_medium=email]

 * Device Specs: Raspberry Pi 5-based, with M2 storage, designed for secure
   local compute and data
   sovereignty.[https://storage.googleapis.com/fathom-static-web-assets/courier/mailers/post-meeting/ico-play-black.png]
   [https://fathom.video/share/o52tuXVsCJxmz3yVBs8aieEWRKxDPuba?tab=summary&timestamp=1316.0&utm_campaign=postmeetingsummary&utm_content=summary_item&utm_medium=email]

 * Network
   Tiers:[https://storage.googleapis.com/fathom-static-web-assets/courier/mailers/post-meeting/ico-play-black.png]
   [https://fathom.video/share/o52tuXVsCJxmz3yVBs8aieEWRKxDPuba?tab=summary&timestamp=1347.0&utm_campaign=postmeetingsummary&utm_content=summary_item&utm_medium=email]
   
   * Fog Computing: Home-based ZKN
     nodes.[https://storage.googleapis.com/fathom-static-web-assets/courier/mailers/post-meeting/ico-play-black.png]
     [https://fathom.video/share/o52tuXVsCJxmz3yVBs8aieEWRKxDPuba?tab=summary&timestamp=1347.0&utm_campaign=postmeetingsummary&utm_content=summary_item&utm_medium=email]
   
   * Mist Computing: Mobile
     clients.[https://storage.googleapis.com/fathom-static-web-assets/courier/mailers/post-meeting/ico-play-black.png]
     [https://fathom.video/share/o52tuXVsCJxmz3yVBs8aieEWRKxDPuba?tab=summary&timestamp=1365.0&utm_campaign=postmeetingsummary&utm_content=summary_item&utm_medium=email]

 * Funding Commitment: ZKN will provide flow funding to support Folk.js
   development, recognizing its value for building on the ZKN
   platform.[https://storage.googleapis.com/fathom-static-web-assets/courier/mailers/post-meeting/ico-play-black.png]
   [https://fathom.video/share/o52tuXVsCJxmz3yVBs8aieEWRKxDPuba?tab=summary&timestamp=1390.0&utm_campaign=postmeetingsummary&utm_content=summary_item&utm_medium=email]


KEYHIVE & CRDT-BASED CONTRACTS

 * KeyHive, from Ink & Switch, enables end-to-end encryption for AutoMerge
   CRDTs.[https://storage.googleapis.com/fathom-static-web-assets/courier/mailers/post-meeting/ico-play-black.png]
   [https://fathom.video/share/o52tuXVsCJxmz3yVBs8aieEWRKxDPuba?tab=summary&timestamp=2586.0&utm_campaign=postmeetingsummary&utm_content=summary_item&utm_medium=email]

 * KeyHive
   Benefits:[https://storage.googleapis.com/fathom-static-web-assets/courier/mailers/post-meeting/ico-play-black.png]
   [https://fathom.video/share/o52tuXVsCJxmz3yVBs8aieEWRKxDPuba?tab=summary&timestamp=2586.0&utm_campaign=postmeetingsummary&utm_content=summary_item&utm_medium=email]
   
   * Performance: Sync is orders of magnitude
     faster.[https://storage.googleapis.com/fathom-static-web-assets/courier/mailers/post-meeting/ico-play-black.png]
     [https://fathom.video/share/o52tuXVsCJxmz3yVBs8aieEWRKxDPuba?tab=summary&timestamp=1739.0&utm_campaign=postmeetingsummary&utm_content=summary_item&utm_medium=email]
   
   * Architecture: Sync servers become stateless, cheap "black
     boxes."[https://storage.googleapis.com/fathom-static-web-assets/courier/mailers/post-meeting/ico-play-black.png]
     [https://fathom.video/share/o52tuXVsCJxmz3yVBs8aieEWRKxDPuba?tab=summary&timestamp=2760.0&utm_campaign=postmeetingsummary&utm_content=summary_item&utm_medium=email]
   
   * Permissions: Uses a capabilities-based model (like a ticket) for granular,
     local
     authorization.[https://storage.googleapis.com/fathom-static-web-assets/courier/mailers/post-meeting/ico-play-black.png]
     [https://fathom.video/share/o52tuXVsCJxmz3yVBs8aieEWRKxDPuba?tab=summary&timestamp=2824.0&utm_campaign=postmeetingsummary&utm_content=summary_item&utm_medium=email]

 * "Smart Contract Analogs": KeyHive's capabilities model allows for building
   contract-like logic (e.g., anonymous polls, access control) directly on
   CRDTs, bypassing traditional blockchain
   overhead.[https://storage.googleapis.com/fathom-static-web-assets/courier/mailers/post-meeting/ico-play-black.png]
   [https://fathom.video/share/o52tuXVsCJxmz3yVBs8aieEWRKxDPuba?tab=summary&timestamp=2490.0&utm_campaign=postmeetingsummary&utm_content=summary_item&utm_medium=email]


WEBGPU VISUALIZATIONS

 * New WebGPU shaders are being explored to create semantic visualizations of
   data
   relationships.[https://storage.googleapis.com/fathom-static-web-assets/courier/mailers/post-meeting/ico-play-black.png]
   [https://fathom.video/share/o52tuXVsCJxmz3yVBs8aieEWRKxDPuba?tab=summary&timestamp=453.0&utm_campaign=postmeetingsummary&utm_content=summary_item&utm_medium=email]

 * Demos:[https://storage.googleapis.com/fathom-static-web-assets/courier/mailers/post-meeting/ico-play-black.png]
   [https://fathom.video/share/o52tuXVsCJxmz3yVBs8aieEWRKxDPuba?tab=summary&timestamp=541.0&utm_campaign=postmeetingsummary&utm_content=summary_item&utm_medium=email]
   
   * Signed Distance Fields (SDFs): Mapping DOM nodes to SDFs for interactive
     morphing.[https://storage.googleapis.com/fathom-static-web-assets/courier/mailers/post-meeting/ico-play-black.png]
     [https://fathom.video/share/o52tuXVsCJxmz3yVBs8aieEWRKxDPuba?tab=summary&timestamp=541.0&utm_campaign=postmeetingsummary&utm_content=summary_item&utm_medium=email]
   
   * Radiance Cascade: Elements emit color "radiance" that blends on proximity
     (e.g., red + blue → purple), visualizing emergent
     properties.[https://storage.googleapis.com/fathom-static-web-assets/courier/mailers/post-meeting/ico-play-black.png]
     [https://fathom.video/share/o52tuXVsCJxmz3yVBs8aieEWRKxDPuba?tab=summary&timestamp=594.0&utm_campaign=postmeetingsummary&utm_content=summary_item&utm_medium=email]

 * Future Use Case: Modeling liquid flows and pipes to visualize funding
   streams.[https://storage.googleapis.com/fathom-static-web-assets/courier/mailers/post-meeting/ico-play-black.png]
   [https://fathom.video/share/o52tuXVsCJxmz3yVBs8aieEWRKxDPuba?tab=summary&timestamp=660.0&utm_campaign=postmeetingsummary&utm_content=summary_item&utm_medium=email]


"INFORMATION SUBSTRATE" MODEL

 * A new model is being explored to break free from rigid application
   silos.[https://storage.googleapis.com/fathom-static-web-assets/courier/mailers/post-meeting/ico-play-black.png]
   [https://fathom.video/share/o52tuXVsCJxmz3yVBs8aieEWRKxDPuba?tab=summary&timestamp=744.0&utm_campaign=postmeetingsummary&utm_content=summary_item&utm_medium=email]

 * Problem: Protocols (e.g., Bluesky's ATProto) support features (e.g., rich
   text) that official apps don't, forcing users into siloed, copy-paste
   workflows.[https://storage.googleapis.com/fathom-static-web-assets/courier/mailers/post-meeting/ico-play-black.png]
   [https://fathom.video/share/o52tuXVsCJxmz3yVBs8aieEWRKxDPuba?tab=summary&timestamp=754.0&utm_campaign=postmeetingsummary&utm_content=summary_item&utm_medium=email]

 * Solution: Treat protocols as "material" that users manipulate with
   "instruments" (tools), allowing for flexible, user-defined
   workflows.[https://storage.googleapis.com/fathom-static-web-assets/courier/mailers/post-meeting/ico-play-black.png]
   [https://fathom.video/share/o52tuXVsCJxmz3yVBs8aieEWRKxDPuba?tab=summary&timestamp=824.0&utm_campaign=postmeetingsummary&utm_content=summary_item&utm_medium=email]


THRESHOLD-BASED FLOW FUNDING (TBFF) DEMO

 * Sean built a TBFF demo in Folk.js using propagators to model funding
   streams.[https://storage.googleapis.com/fathom-static-web-assets/courier/mailers/post-meeting/ico-play-black.png]
   [https://fathom.video/share/o52tuXVsCJxmz3yVBs8aieEWRKxDPuba?tab=summary&timestamp=1981.0&utm_campaign=postmeetingsummary&utm_content=summary_item&utm_medium=email]

 * TBFF
   Logic:[https://storage.googleapis.com/fathom-static-web-assets/courier/mailers/post-meeting/ico-play-black.png]
   [https://fathom.video/share/o52tuXVsCJxmz3yVBs8aieEWRKxDPuba?tab=summary&timestamp=2218.0&utm_campaign=postmeetingsummary&utm_content=summary_item&utm_medium=email]
   
   * Users set a min_threshold and
     max_threshold.[https://storage.googleapis.com/fathom-static-web-assets/courier/mailers/post-meeting/ico-play-black.png]
     [https://fathom.video/share/o52tuXVsCJxmz3yVBs8aieEWRKxDPuba?tab=summary&timestamp=2218.0&utm_campaign=postmeetingsummary&utm_content=summary_item&utm_medium=email]
   
   * Funds received up to min_threshold are
     kept.[https://storage.googleapis.com/fathom-static-web-assets/courier/mailers/post-meeting/ico-play-black.png]
     [https://fathom.video/share/o52tuXVsCJxmz3yVBs8aieEWRKxDPuba?tab=summary&timestamp=2325.0&utm_campaign=postmeetingsummary&utm_content=summary_item&utm_medium=email]
   
   * Funds between min_threshold and max_threshold are split between the
     recipient and their "flow forward"
     contacts.[https://storage.googleapis.com/fathom-static-web-assets/courier/mailers/post-meeting/ico-play-black.png]
     [https://fathom.video/share/o52tuXVsCJxmz3yVBs8aieEWRKxDPuba?tab=summary&timestamp=2291.0&utm_campaign=postmeetingsummary&utm_content=summary_item&utm_medium=email]
   
   * Funds above max_threshold are entirely flowed
     forward.[https://storage.googleapis.com/fathom-static-web-assets/courier/mailers/post-meeting/ico-play-black.png]
     [https://fathom.video/share/o52tuXVsCJxmz3yVBs8aieEWRKxDPuba?tab=summary&timestamp=2291.0&utm_campaign=postmeetingsummary&utm_content=summary_item&utm_medium=email]


NEXT STEPS

 * Jeff: Draft a proposal for the ZKN flow funding
   sub-DAO.[https://storage.googleapis.com/fathom-static-web-assets/courier/mailers/post-meeting/ico-play-black.png]
   [https://fathom.video/share/o52tuXVsCJxmz3yVBs8aieEWRKxDPuba?tab=summary&timestamp=1493.0&utm_campaign=postmeetingsummary&utm_content=summary_item&utm_medium=email]

 * Jeff: Connect the Folk.js team with ZKN once their ZKVM is
   available.[https://storage.googleapis.com/fathom-static-web-assets/courier/mailers/post-meeting/ico-play-black.png]
   [https://fathom.video/share/o52tuXVsCJxmz3yVBs8aieEWRKxDPuba?tab=summary&timestamp=1576.0&utm_campaign=postmeetingsummary&utm_content=summary_item&utm_medium=email]

 * Orion: Continue KeyHive integration with Folk.js and explore CRDT-based
   contract
   analogs.[https://storage.googleapis.com/fathom-static-web-assets/courier/mailers/post-meeting/ico-play-black.png]
   [https://fathom.video/share/o52tuXVsCJxmz3yVBs8aieEWRKxDPuba?tab=summary&timestamp=2490.0&utm_campaign=postmeetingsummary&utm_content=summary_item&utm_medium=email]

 * Chris: Continue exploring the "information substrate"
   model.[https://storage.googleapis.com/fathom-static-web-assets/courier/mailers/post-meeting/ico-play-black.png]
   [https://fathom.video/share/o52tuXVsCJxmz3yVBs8aieEWRKxDPuba?tab=summary&timestamp=744.0&utm_campaign=postmeetingsummary&utm_content=summary_item&utm_medium=email]

 * All: Use the TBFF demo to dogfood the flow funding
   concept.[https://storage.googleapis.com/fathom-static-web-assets/courier/mailers/post-meeting/ico-play-black.png]
   [https://fathom.video/share/o52tuXVsCJxmz3yVBs8aieEWRKxDPuba?tab=summary&timestamp=2361.0&utm_campaign=postmeetingsummary&utm_content=summary_item&utm_medium=email]

View Meeting →
[https://fathom.video/share/o52tuXVsCJxmz3yVBs8aieEWRKxDPuba?tab=summary&utm_campaign=postmeetingsummary&utm_content=view_recording_button&utm_medium=email]

[https://storage.googleapis.com/fathom-static-web-assets/courier/mailers/post-meeting/robot.png]
Ask Fathom! Ask our AI Assistant for answers and insights. It's ChatGPT for your
meetings! Try Ask Fathom →
[https://fathom.video/share/o52tuXVsCJxmz3yVBs8aieEWRKxDPuba?tab=ask_fathom&utm_campaign=postmeetingsummary&utm_content=ask_fathom_footer&utm_medium=email]

[https://storage.googleapis.com/fathom-static-web-assets/courier/mailers/post-meeting/ask-fathom-screenshot.png]

Never take notes again. Sign up for Free
[https://fathom.video/invite/uZP-Uw?utm_medium=email&utm_campaign=postmeetingsummary&utm_content=footer]
🎁 Referral bonus: Sign up now and unlock a free month of Premium for you and
Jeff

[https://storage.googleapis.com/fathom-static-web-assets/courier/mailers/post-meeting/rating.png]
https://www.g2.com/products/fathom-2021-09-22/reviews
