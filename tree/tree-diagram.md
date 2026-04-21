graph TD
    START["START<br/>Good evening. Let's look at your day."]
    A1_INTRO["A1_INTRO<br/>How would you describe today?"]
    A1_OPEN["A1_OPEN<br/>One word for today?<br/>- Productive<br/>- Mixed<br/>- Tough<br/>- Draining"]
    
    start_to_a1["START → A1_INTRO → A1_OPEN"]
    
    A1_DECISION{"Router:<br/>Productive/Mixed<br/>vs<br/>Tough/Draining"}
    
    A1_Q_HIGH["A1_Q_AGENCY_HIGH<br/>What was YOUR role<br/>in good things?<br/>- Prepared<br/>- Adapted<br/>- Took initiative<br/>- Got help"]
    
    A1_Q_LOW["A1_Q_AGENCY_LOW<br/>When hard, your instinct?<br/>- Controlled what I could<br/>- Felt stuck<br/>- Pushed harder<br/>- Looked for help"]
    
    A1_DECISION_2{"Router:<br/>Solo agency<br/>vs<br/>Collaborative"}
    
    A1_DECISION_3{"Router:<br/>Found agency<br/>vs<br/>Felt stuck"}
    
    A1_REFLECT_INT["A1_REFLECT_INTERNAL<br/>You stayed in driver's seat<br/>signal: axis1:internal"]
    
    A1_REFLECT_EXT["A1_REFLECT_EXTERNAL<br/>You made choices, even small<br/>signal: axis1:external"]
    
    A1_REFLECT_COLLAB["A1_REFLECT_COLLABORATIVE<br/>Asking help is mature agency<br/>signal: axis1:internal"]
    
    BRIDGE_1_2["BRIDGE_1_2<br/>Now shift to what you gave<br/>vs what you needed"]
    
    A2_OPEN["A2_OPEN<br/>Meaningful interaction?<br/>- Helped<br/>- Taught<br/>- Asked for help<br/>- Felt unrecognized"]
    
    A2_DECISION{"Router:<br/>Contribution<br/>vs<br/>Neutral<br/>vs<br/>Entitlement"}
    
    A2_Q_CONTRIB["A2_Q_CONTRIBUTION<br/>After helping/teaching?<br/>- Felt good<br/>- Tired but worth it<br/>- Just do them<br/>- Got appreciated"]
    
    A2_Q_MUTUAL["A2_Q_MUTUAL<br/>When you got support?<br/>- Moved forward<br/>- Felt grateful<br/>- Had to ask often<br/>- Should handle alone"]
    
    A2_Q_ENT["A2_Q_ENTITLEMENT<br/>Lack of recognition?<br/>- Do better<br/>- Blame others<br/>- Wrong place?<br/>- Did my best?"]
    
    A2_DECISION_2{"Router:<br/>Contribution<br/>Dominant<br/>vs<br/>Entitlement<br/>Dominant"}
    
    CONTRIB_REFLECT["CONTRIBUTION_DOMINANT<br/>You gave today<br/>signal: axis2:contribution"]
    
    ENT_REFLECT["ENTITLEMENT_DOMINANT<br/>Notice what you're proving<br/>signal: axis2:entitlement"]
    
    BRIDGE_2_3["BRIDGE_2_3<br/>Whose world in your frame?"]
    
    A3_OPEN["A3_OPEN<br/>Biggest challenge/win?<br/>- My own<br/>- Team's<br/>- Someone harder<br/>- Customer/end user"]
    
    A3_DECISION{"Router:<br/>Self-centric<br/>vs<br/>Other-focused"}
    
    A3_Q_SELF["A3_Q_SELF<br/>Self-focus effect?<br/>- Sharp & accountable<br/>- Anxious<br/>- Volatile mood<br/>- Isolated"]
    
    A3_Q_OTHER["A3_Q_OTHER<br/>Broader frame effect?<br/>- Problems smaller<br/>- More energy<br/>- Clarity<br/>- Harder"]
    
    A3_DECISION_2{"Router:<br/>Self-centric<br/>vs<br/>Other-focused"}
    
    A3_REFLECT_SELF["A3_REFLECT_SELF<br/>Meaning lives in the bigger thing<br/>signal: axis3:self_centric"]
    
    A3_REFLECT_OTHER["A3_REFLECT_OTHER<br/>Wide frame = more effective<br/>signal: axis3:altrocentric"]
    
    SUMMARY["SUMMARY<br/>You leaned {axis1} on agency<br/>You showed {axis2} on contribution<br/>Your frame was {axis3}<br/>That's what you chose to notice"]
    
    END["END<br/>See you tomorrow."]
    
    START --> A1_INTRO
    A1_INTRO --> A1_OPEN
    A1_OPEN --> A1_DECISION
    A1_DECISION -->|Productive/Mixed| A1_Q_HIGH
    A1_DECISION -->|Tough/Draining| A1_Q_LOW
    A1_Q_HIGH --> A1_DECISION_2
    A1_Q_LOW --> A1_DECISION_3
    A1_DECISION_2 -->|Solo| A1_REFLECT_INT
    A1_DECISION_2 -->|Help| A1_REFLECT_COLLAB
    A1_DECISION_3 -->|Found agency| A1_REFLECT_INT
    A1_DECISION_3 -->|Stuck| A1_REFLECT_EXT
    A1_REFLECT_INT --> BRIDGE_1_2
    A1_REFLECT_EXT --> BRIDGE_1_2
    A1_REFLECT_COLLAB --> BRIDGE_1_2
    BRIDGE_1_2 --> A2_OPEN
    A2_OPEN --> A2_DECISION
    A2_DECISION -->|Helped/Taught| A2_Q_CONTRIB
    A2_DECISION -->|Asked| A2_Q_MUTUAL
    A2_DECISION -->|Unrecognized| A2_Q_ENT
    A2_Q_CONTRIB --> A2_DECISION_2
    A2_Q_MUTUAL --> A2_DECISION_2
    A2_Q_ENT --> A2_DECISION_2
    A2_DECISION_2 -->|Contribution| CONTRIB_REFLECT
    A2_DECISION_2 -->|Entitlement| ENT_REFLECT
    CONTRIB_REFLECT --> BRIDGE_2_3
    ENT_REFLECT --> BRIDGE_2_3
    BRIDGE_2_3 --> A3_OPEN
    A3_OPEN --> A3_DECISION
    A3_DECISION -->|Self| A3_Q_SELF
    A3_DECISION -->|Others| A3_Q_OTHER
    A3_Q_SELF --> A3_DECISION_2
    A3_Q_OTHER --> A3_DECISION_2
    A3_DECISION_2 -->|Self-centric| A3_REFLECT_SELF
    A3_DECISION_2 -->|Other-focused| A3_REFLECT_OTHER
    A3_REFLECT_SELF --> SUMMARY
    A3_REFLECT_OTHER --> SUMMARY
    SUMMARY --> END
    
    style START fill:#e1f5e1
    style END fill:#ffe1e1
    style SUMMARY fill:#fff3e1
    style A1_REFLECT_INT fill:#e1e5ff
    style A1_REFLECT_EXT fill:#e1e5ff
    style A1_REFLECT_COLLAB fill:#e1e5ff
    style CONTRIB_REFLECT fill:#e1ffe1
    style ENT_REFLECT fill:#e1ffe1
    style A3_REFLECT_SELF fill:#e1f5ff
    style A3_REFLECT_OTHER fill:#e1f5ff
