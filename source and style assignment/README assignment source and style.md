# Assignment 1: Inspecting the Cultural Web

Site inspected: LA84 Foundation Digital Library
URL: https://digital.la84.org/digital/
**Parent organization:** [LA84 Foundation](https://la84.org/) — a Los Angeles nonprofit created in 1985 to manage Southern California's share of the 1984 Summer Olympics surplus, and the operator of what is often called the world's largest privately funded sports library.


## What web technologies were used to build the tool?

The digital library is built on CONTENTdm, a proprietary "software as a service" digital-collection platform owned and hosted by OCLC (Online Computer Library Center), the same nonprofit that runs WorldCat. This is the reasoning for limited github repo access. 

- The page `<title>` and page metadata  read "CONTENTdm," and every collection page displays a message that says, "Javascript Required — to experience full interactivity, please enable Javascript in your browser."
- There are no visible `.html`, `.css`, or `.js` filenames** in the URLs at all. Instead, the URL pattern looks like `digital.la84.org/digital/collection/p17103coll11` — `p17103coll11` is a CONTENTdm **collection alias**, an internal ID the software generates, not a file you could locate on a server. This is very different from a hand-built static site where you might see `about.html` or `main.js` in the address bar.
When I searched for a publib github repo nothing comes up for LA84. 

There wasn't really any files I didn't recognize, they all mainly made good sense to me.


## Who built this website?

The platform itself was built and is maintained by online computer library center
The content is managed by the LA84 staff. Wayne Willson, the VP of communication, and Anita DeFrantz the presiednt of the foundation. 

## Screenshots

![LA84 Digital Library homepage](images/la84-homepage.png)

![LA84 Digital Library collection page](images/la84-collection-page.png)

![Browser dev tools open on a LA84 collection page, showing the CONTENTdm JavaScript gate](images/la84-devtools.png)

*(Screenshots above are wired up but not yet added — see "Getting the screenshots" below.)*

### Getting the screenshots

Save exactly these three files into `source-and-style/images/` — the README above already points at these filenames, so nothing else needs editing once they're in place:

1. **`la84-homepage.png`** — open https://digital.la84.org/digital/ and screenshot the landing page (including the moment it shows the "Javascript Required" message, if you can catch it).
2. **`la84-collection-page.png`** — click into any collection (e.g. the Olympic Official Reports or Olympian Oral History collection) and screenshot that page.
3. **`la84-devtools.png`** — on that same collection page, open your browser's dev tools (right-click → Inspect, or F12 / Cmd+Option+I) to the **Network** or **Elements** tab, and screenshot the whole window so both the page and the dev tools panel are visible. This is the shot that actually shows the CONTENTdm/JS evidence described above.

How to save a screenshot on your OS:
- **Mac:** `Cmd+Shift+4`, drag to select the area, the file saves to your Desktop — then move/rename it into `images/`.
- **Windows:** `Win+Shift+S`, select the area, paste into Paint (`Ctrl+V`) and save as PNG into `images/`.
- **Chromebook:** `Ctrl+Shift+ Show windows key`, select the area.

---

 Assignment 2: Styling the Cultural Web


in index folder