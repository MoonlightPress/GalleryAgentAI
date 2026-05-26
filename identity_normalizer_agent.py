import streamlit as st
import json
import os


st.set_page_config(
    page_title="Artist Career Dashboard",
    layout="wide"
)


def load_text(path, fallback=""):
    if not os.path.exists(path):
        return fallback
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def load_json(path, fallback):
    if not os.path.exists(path):
        return fallback
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


st.title("Artist Career Dashboard")

tabs = st.tabs([
    "Artist Dossier",
    "Market Report",
    "Opportunities",
    "Add Opportunity",
    "CRM",
    "Add Contact",
    "Email Drafts",
    "Quests",
    "Chinese Summary",
    "Japanese Outreach",
])


with tabs[0]:
    st.header("Artist Dossier")
    st.markdown(load_text("artist_dossier.md", "No artist dossier found."))


with tabs[1]:
    st.header("Market / Strategy Report")
    st.markdown(load_text("final_gallery_report.md", "No market report found."))

with tabs[2]:
    st.header("Opportunities")
   
    opportunities = load_json("memory/opportunities.json", [])
    total_opps = len(opportunities)
    sent_count = len([
        o for o in opportunities
        if o.get("status") == "sent"
    ])

    followup_count = len([
        o for o in opportunities
        if o.get("status") == "follow_up_later"
    ])

    active_count = len([
        o for o in opportunities
        if o.get("status") not in [
            "sent",
            "skipped"
        ]
    ])

    high_priority_count = len([
        o for o in opportunities
        if o.get("priority") == "A"
    ])

    momentum_values = []

    for o in opportunities:

        fit = o.get("fit_score", 5)
        urgency = o.get("urgency_score", 5)
        effort = o.get("effort_score", 5)
        strategic = o.get("strategic_score", 5)
        emotional = o.get("emotional_resistance", 5)

        momentum = (
            fit
            + urgency
            + strategic
            - effort
            - emotional
        )

        momentum_values.append(momentum)

    average_momentum = 0

    if momentum_values:
        average_momentum = round(
            sum(momentum_values) / len(momentum_values),
            1
        )

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    col1.metric("Total", total_opps)
    col2.metric("Active", active_count)
    col3.metric("Sent", sent_count)
    col4.metric("Follow Up", followup_count)
    col5.metric("Priority A", high_priority_count)
    col6.metric("Avg Momentum", average_momentum)
    st.markdown("---")
    st.subheader("Daily Quest")

    best_opportunity = None
    best_score = -999

    for o in opportunities:

        fit = o.get("fit_score", 5)
        urgency = o.get("urgency_score", 5)
        effort = o.get("effort_score", 5)
        strategic = o.get("strategic_score", 5)
        emotional = o.get("emotional_resistance", 5)

        score = (
            fit * 2
            + urgency
            + strategic * 2
            - effort
            - emotional
        )

        if o.get("status") in [
            "sent",
            "skipped"
        ]:
            continue

        if score > best_score:
            best_score = score
            best_opportunity = o

    if best_opportunity:

        st.success(
            f"""
Today's Best Quest:

Research or advance:
{best_opportunity.get("name", "")}

Why:
{best_opportunity.get("why_fit", "")}

Recommended next action:
{best_opportunity.get("next_action", "")}
"""
        )
    col_filter1, col_filter2 = st.columns(2)

    with col_filter1:
        status_filter = st.selectbox(
            "Filter by status",
            [
                "all",
                "research_needed",
                "ready_to_review",
                "sent",
                "response_received",
                "follow_up_later",
                "skipped"
            ]
        )

    with col_filter2:
        priority_filter = st.selectbox(
            "Filter by priority",
            [
                "all",
                "A",
                "B",
                "C"
            ]
        )

    
    def save_opportunities(data):
        with open("memory/opportunities.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    if not opportunities:
        st.info("No structured opportunities yet.")
    else:
        for i, opp in enumerate(opportunities):
            if status_filter != "all" and opp.get("status", "") != status_filter:
                continue

            if priority_filter != "all" and opp.get("priority", "") != priority_filter:
                continue
            
            with st.expander(opp.get("name", "Unnamed opportunity")):
                st.write("**Type:**", opp.get("type", ""))
                st.write("**City:**", opp.get("city", ""))
                st.write("**Country:**", opp.get("country", ""))
                st.write("**Priority:**", opp.get("priority", ""))
                st.write("**Fit Score:**", opp.get("fit_score", ""))
                st.write("**Urgency Score:**", opp.get("urgency_score", ""))
                st.write("**Effort Required:**", opp.get("effort_score", ""))
                st.write("**Strategic Value:**", opp.get("strategic_score", ""))
                st.write("**Emotional Resistance:**", opp.get("emotional_resistance", ""))
                fit = opp.get("fit_score", 5)
                urgency = opp.get("urgency_score", 5)
                effort = opp.get("effort_score", 5)
                strategic = opp.get("strategic_score", 5)
                emotional = opp.get("emotional_resistance", 5)

                momentum_score = (
                    fit
                    + urgency
                    + strategic
                    - effort
                    - emotional
                )

                if momentum_score >= 15:
                    next_action_advice = "Strong candidate. Move soon before momentum fades."

                elif momentum_score >= 8:
                    next_action_advice = "Worth pursuing, but reduce friction before acting."

                else:
                    next_action_advice = "Low-energy opportunity. Only pursue if emotionally easy."

                st.info(f"Best Next Action: {next_action_advice}")
                st.write("**Status:**", opp.get("status", ""))
                st.write("**Official website:**", opp.get("official_website", ""))
                st.write("**Contact page:**", opp.get("contact_page", ""))
                st.write("**Contact email:**", opp.get("contact_email", ""))
                if opp.get("preview_image"):
                    st.image(
                        opp.get("preview_image"),
                        width=300
                    )
                st.write("**Why fit:**", opp.get("why_fit", ""))
                st.write("**Next action:**", opp.get("next_action", ""))
                st.write("**Risk notes:**", opp.get("risk_notes", ""))

                notes_key = f"notes_{i}"

                new_notes = st.text_area(
                    "Curator Notes",
                    value=opp.get("curator_notes", ""),
                    key=notes_key,
                    height=120
                )

                if st.button("Save Notes", key=f"save_notes_{i}"):
                    opportunities[i]["curator_notes"] = new_notes
                    save_opportunities(opportunities)
                    st.success("Notes saved.")

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    if st.button("Email sent", key=f"sent_{i}"):
                        opportunities[i]["status"] = "sent"
                        opportunities[i]["last_contacted"] = "2026-05-24"
                        save_opportunities(opportunities)
                        st.rerun()

                with col2:
                    if st.button("Response received", key=f"response_{i}"):
                        opportunities[i]["status"] = "response_received"
                        save_opportunities(opportunities)
                        st.rerun()

                with col3:
                    if st.button("Follow up later", key=f"follow_{i}"):
                        opportunities[i]["status"] = "follow_up_later"
                        opportunities[i]["follow_up_note"] = "Follow up later."
                        save_opportunities(opportunities)
                        st.rerun()

                with col4:
                    if st.button("Skip", key=f"skip_{i}"):
                        opportunities[i]["status"] = "skipped"
                        save_opportunities(opportunities)
                        st.rerun()
                        
                        
                        st.markdown("---")

                if st.button("Generate Multilingual Outreach", key=f"generate_outreach_{i}"):

                    import subprocess

                    with st.spinner("Generating multilingual outreach..."):

                        result = subprocess.run(
                            ["python", "outreach_email_agent.py", str(i)],
                            capture_output=True,
                            text=True
                        )

                    if result.returncode != 0:
                        st.error("Outreach generation failed.")
                        st.code(result.stderr)
                    else:
                        st.success("Multilingual outreach generated.")

                    opportunities = load_json("memory/opportunities.json", [])

                    opp = opportunities[i]   
                    st.rerun()
               
                outreach = opp.get("multilingual_outreach", {})

                if outreach:
                    st.markdown("---")
                    st.subheader("Multilingual Outreach")

                    st.markdown("### Artist Summary - Chinese")
                    st.text_area(
                        "Chinese Summary",
                        value=outreach.get("artist_summary_zh", ""),
                        height=250,
                        key=f"artist_summary_zh_{i}"
                    )

                    st.markdown("### Target Language Email")
                    st.write("**Language:**", outreach.get("target_language", ""))
                    st.write("**Subject:**", outreach.get("email_subject_target_language", ""))

                    st.text_area(
                        "Outreach Email",
                        value=outreach.get("outreach_email_target_language", ""),
                        height=320,
                        key=f"target_email_{i}"
                    )

                    st.markdown("### English Translation")
                    st.write("**Subject:**", outreach.get("email_subject_en_translation", ""))

                    st.text_area(
                        "English Translation",
                        value=outreach.get("outreach_email_en_translation", ""),
                        height=320,
                        key=f"email_translation_{i}"
                    )

                    st.markdown("### Attachment Checklist")
                    for item in outreach.get("attachment_checklist_en", []):
                        st.write("- " + item)

                    st.markdown("### Human Verification Needed")
                    for item in outreach.get("human_verification_needed", []):
                        st.warning(item)
                    
with tabs[3]:

    st.header("Add Opportunity")

    new_name = st.text_input("Name")
    new_type = st.text_input("Type")
    new_city = st.text_input("City")
    new_country = st.text_input("Country")
    new_website = st.text_input(
    "Official Website",
    key="opportunity_official_website"
)
    new_contact = st.text_input(
    "Contact Email",
    key="opportunity_contact_email"
)
    new_image = st.text_input("Preview Image Path")

    new_fit = st.text_area(
        "Why This Fits",
        height=120
    )

    new_action = st.text_area(
        "Next Action",
        height=120
    )

    new_risks = st.text_area(
        "Risk Notes",
        height=120
    )

    fit_score = st.slider(
        "Fit Score",
        1,
        10,
        5
    )

    urgency_score = st.slider(
        "Urgency Score",
        1,
        10,
        5
    )

    effort_score = st.slider(
        "Effort Required",
        1,
        10,
        5
    )

    strategic_score = st.slider(
        "Strategic Value",
        1,
        10,
        5
    )

    emotional_resistance = st.slider(
        "Emotional Resistance",
        1,
        10,
        5
    )
    

    if st.button("Save Opportunity"):

        opportunities = load_json(
            "memory/opportunities.json",
            []
        )
        weighted_score = (
            fit_score * 2
            + urgency_score
            + strategic_score * 2
            - effort_score
            - emotional_resistance
        )

        if weighted_score >= 25:
            calculated_priority = "A"
        elif weighted_score >= 15:
            calculated_priority = "B"
        else:
            calculated_priority = "C"
        new_opportunity = {
            "fit_score": fit_score,
            "urgency_score": urgency_score,
            "effort_score": effort_score,
            "strategic_score": strategic_score,
            "emotional_resistance": emotional_resistance,
            "preview_image": new_image,
            "name": new_name,
            "type": new_type,
            "city": new_city,
            "country": new_country,
            "official_website": new_website,
            "contact_email": new_contact,
            "status": "research_needed",
            "priority": calculated_priority,
            "why_fit": new_fit,
            "next_action": new_action,
            "risk_notes": new_risks
        }

        opportunities.append(new_opportunity)

        with open(
            "memory/opportunities.json",
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(
                opportunities,
                f,
                indent=2,
                ensure_ascii=False
            )

        st.success("Opportunity saved.")

with tabs[4]:
    st.header("CRM / Contacts")
    contacts = load_json("memory/contact_memory.json", {"contacts": []}).get("contacts", [])

    if not contacts:
        st.info("No contacts yet.")
    else:
        for contact in contacts:
            analysis = contact.get("crm_analysis", {})
            with st.expander(contact.get("name", "Unnamed contact")):
                st.write("**Type:**", contact.get("type", ""))
                st.write("**City:**", contact.get("city", ""))
                st.write("**Country:**", contact.get("country", ""))
                st.write("**Status:**", contact.get("status", ""))
                st.write("**Priority:**", analysis.get("priority", ""))
                st.write("**Next action:**", analysis.get("next_action", ""))
                st.write("**Follow-up timing:**", analysis.get("follow_up_timing", ""))
                st.write("**Risk notes:**", analysis.get("risk_notes", ""))
                web = contact.get("web_verification", {})
                st.write("**Official website:**", contact.get("official_website", ""))
                st.write("**Contact page:**", contact.get("contact_page", ""))
                st.write("**Submission page:**", contact.get("submission_page", ""))
                st.write("**Contact email:**", contact.get("contact_email", ""))
                st.write("**Instagram:**", web.get("instagram", ""))
                st.write("**Verification status:**", web.get("verification_status", ""))
                st.write("**Last verified:**", web.get("last_verified", ""))

with tabs[5]:

    st.header("Add Contact")

    contact_name = st.text_input("Contact Name")
    contact_type = st.text_input("Contact Type")
    contact_city = st.text_input("Contact City")
    contact_country = st.text_input("Contact Country")
    contact_email = st.text_input(
    "Contact Email",
    key="contact_contact_email"
)
    contact_website = st.text_input(
    "Official Website",
    key="contact_official_website"
)
    contact_page = st.text_input("Contact Page")

    contact_notes = st.text_area(
        "Contact Notes",
        height=120
    )

    if st.button("Save Contact"):

        contact_memory = load_json(
            "memory/contact_memory.json",
            {"contacts": []}
        )

        new_contact = {
            "name": contact_name,
            "type": contact_type,
            "city": contact_city,
            "country": contact_country,
            "contact_email": contact_email,
            "official_website": contact_website,
            "contact_page": contact_page,
            "status": "not_contacted",
            "response_received": False,
            "notes": contact_notes
        }

        contact_memory["contacts"].append(new_contact)

        with open(
            "memory/contact_memory.json",
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(
                contact_memory,
                f,
                indent=2,
                ensure_ascii=False
            )

        st.success("Contact saved.")

with tabs[6]:
    st.header("Email Drafts")
    st.markdown(load_text("email_drafts.md", "No email drafts found."))


with tabs[7]:
    st.header("Quest Report")
    st.markdown(load_text("quest_report.md", "No quest report found."))


with tabs[8]:
    st.header("Chinese Summary")
    st.info("Placeholder: Chinese artist-facing summary will go here.")


with tabs[9]:
    st.header("Japanese Outreach")
    st.info("Placeholder: Japanese gallery outreach support will go here.")