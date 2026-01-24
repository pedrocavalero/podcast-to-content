---
name: linkedin-post-generator
description: Generates LinkedIn posts from YouTube video subtitles following proven engagement strategies. Extracts 5 main topics relevant to software developers and creates multiple post variations per topic. Use when repurposing video content for LinkedIn authority building.
allowed-tools: [Read, Write, Glob, Bash, AskUserQuestion]
---

# LinkedIn Post Generator

## Overview

This skill transforms YouTube video subtitles into high-engagement LinkedIn posts designed for software developer audiences. It follows proven LinkedIn strategies for native content that maximizes visibility and engagement.

## Core Strategy

### Content Philosophy
- **Native LinkedIn content wins**: Write posts optimized for LinkedIn, not just transcripts
- **One idea per post**: Break complex topics into digestible, focused posts
- **Hook-first writing**: First 2 lines must grab attention in mobile feed
- **Value-driven**: Each post provides actionable insights
- **Authority building**: Positions you as a thought leader

### Post Types
1. **Insight Posts** (Monday): Main concept with data/findings
2. **Story Posts** (Wednesday): Real experiences and case studies
3. **Quick Tips** (Friday): Actionable takeaways
4. **Contrarian Takes**: Challenge common beliefs
5. **Personal Angle**: Vulnerable, relatable experiences

## Instructions

### Step 1: Read and Analyze Subtitles

1. **Locate the SRT file**:
   ```bash
   ls {VIDEO_DIR}/download/*.srt
   ```

2. **Read the subtitle file**:
   - Parse the SRT format
   - Extract the actual spoken content
   - Remove timestamps and line numbers

3. **Understand the content**:
   - Identify main themes discussed
   - Note key insights, stories, examples
   - Find statistics, data points, quotes
   - Recognize contrarian opinions
   - Spot personal anecdotes

### Step 2: Extract 5 Main Topics

**Criteria for topic selection** (optimized for software developers):
- **Relevance**: Directly applicable to developer work/career
- **Specificity**: Concrete, not abstract concepts
- **Actionability**: Provides practical value
- **Uniqueness**: Offers fresh perspective or insight
- **Engagement potential**: Likely to spark discussion

**Topic categories to prioritize**:
- Technical skills and best practices
- Career development and growth
- Team dynamics and collaboration
- Tools and productivity
- Architecture and system design
- AI and emerging technologies
- Work-life balance and remote work
- Learning strategies
- Common mistakes and how to avoid them
- Contrarian takes on popular trends

**Output format**:
```
Topic 1: [Specific, compelling title]
- Key insight: [Main takeaway]
- Audience pain point: [What problem this solves]
- Post angle: [How to present this]

Topic 2: ...
```

### Step 3: Present Strategy for Approval

**Use AskUserQuestion to present**:

```
I've analyzed the video subtitles and identified 5 main topics for LinkedIn posts targeting software developers:

1. [Topic 1 Title]
   - Main insight: [Brief description]
   - Why it matters: [Value proposition]

2. [Topic 2 Title]
   - Main insight: [Brief description]
   - Why it matters: [Value proposition]

...

For each topic, I'll create 3-4 post variations:
- Insight/Data-driven post
- Story/Experience post
- Quick tip/Actionable post
- Discussion/Question post (if applicable)

Total: 15-20 LinkedIn posts optimized for engagement.

Posting schedule suggestion:
- Week 1: Topic 1 (3 posts: Mon/Wed/Fri)
- Week 2: Topic 2 (3 posts: Mon/Wed/Fri)
...

Would you like me to:
A) Proceed with these topics as planned
B) Adjust/replace specific topics (which ones?)
C) Change the focus or angle
```

**Questions to clarify**:
- Tone preference: Professional, conversational, technical, mix?
- Personal pronouns: "I", "we", or third-person?
- Length preference: Short (200-300 words) or Medium (400-500 words)?
- Include emojis: Yes/No/Sparingly?
- Call-to-action: Link to blog, ask questions, both?

### Step 4: Generate LinkedIn Posts

**For each topic, create 3-4 posts following these formulas**:

#### Formula A: The Insight Post
```
[Attention-grabbing hook - contrarian/surprising statement]

[Context in 2-3 lines]

Here's what [audience] needs to know:

→ Point 1
→ Point 2
→ Point 3

[Conclusion or implication]

[Optional: Link in comments / Question for engagement]
```

#### Formula B: The Story Post
```
[Unexpected opening - outcome or problem]

[Story context - what happened]

The result? [Outcome]

Here's what worked/didn't work:

• Point 1
• Point 2
• Point 3

[Takeaway or lesson learned]

[Engagement question]
```

#### Formula C: The Contrarian Take
```
Unpopular opinion:

[Bold statement that challenges common belief]

Here's why:

1. Reason 1
2. Reason 2
3. Reason 3

Instead, try [your approach]

[Question to spark debate]
```

#### Formula D: Quick Tip
```
[Problem statement or opportunity]

Most developers [common mistake/missed opportunity].

Here's what actually works:

✓ Tip 1
✓ Tip 2
✓ Tip 3

[Call to action or question]
```

#### Formula E: Personal/Vulnerable
```
I used to think [common belief].

Wrong. [Why it was wrong]

After [experience/research], here's what I learned:

• Learning 1
• Learning 2
• Learning 3

[Relatable question or sharing prompt]
```

### Step 5: Structure Each Post

**Essential elements**:

1. **Hook (First 2 lines)**:
   - Scroll-stopping statement
   - Visible in mobile preview
   - Creates curiosity gap
   - Examples: Bold claim, surprising stat, contrarian opinion, personal story opening

2. **Body (Middle section)**:
   - Keep paragraphs 1-2 lines max
   - Use bullet points (→, •, ✓)
   - Add white space for readability
   - Include specific examples/numbers
   - Avoid jargon unless audience-specific

3. **Close (Last 2-3 lines)**:
   - Strong takeaway or conclusion
   - Engagement question
   - "Link in comments" (if applicable)
   - Keep it conversational

4. **First Comment** (to be added when posting):
   ```
   [Brief elaboration or additional context]

   Full article/video: [URL]

   [Follow-up question or call-to-action]
   ```

### Step 6: Organize and Save Posts

**Directory structure**:
```
{VIDEO_DIR}/linkedin/
├── README.md (overview and posting schedule)
├── topic-1-{topic-slug}/
│   ├── post-1-insight.md
│   ├── post-2-story.md
│   ├── post-3-quick-tip.md
│   └── post-4-discussion.md
├── topic-2-{topic-slug}/
│   ├── post-1-insight.md
│   ├── post-2-story.md
│   └── post-3-quick-tip.md
...
```

**Post file format**:
```markdown
# [Post Title/Topic]

**Type**: Insight / Story / Quick Tip / Contrarian / Personal
**Target Audience**: Software Developers
**Estimated Engagement**: High / Medium
**Hashtags**: #SoftwareEngineering #TechCareers #Coding [add 2-3 more relevant]
**Best Posting Time**: Monday 8 AM / Wednesday 12 PM / Friday 5 PM

---

## Main Post

[The actual LinkedIn post text - copy-paste ready]

---

## First Comment (Add immediately after posting)

[Comment with link and engagement prompt]

---

## Engagement Strategy

- Respond to all comments in first 2 hours
- Tag relevant connections who've discussed this topic
- Share in relevant LinkedIn groups
- Monitor which hook style performs best

---

## Metrics to Track

- Impressions
- Engagement rate
- Comments (quality and quantity)
- Shares
- Click-through to blog/video

---

## Variations (Optional)

### Shorter Version (if engagement is low)
[Condensed 200-word version]

### Longer Version (if engagement is high)
[Expanded 600-word version with more examples]
```

**README.md format**:
```markdown
# LinkedIn Posts - [Video Title]

Source: [YouTube URL]
Generated: [Date]
Total Posts: [Number]
Topics Covered: [Number]

## Topics Overview

1. **[Topic 1]** - [One-line description] (3 posts)
2. **[Topic 2]** - [One-line description] (4 posts)
...

## Suggested Posting Schedule

### Week 1: [Topic 1]
- **Monday 8 AM**: [Post 1 - Insight]
- **Wednesday 12 PM**: [Post 2 - Story]
- **Friday 5 PM**: [Post 3 - Quick Tip]

### Week 2: [Topic 2]
- **Monday 8 AM**: [Post 1 - Insight]
...

## Performance Tracking

| Post | Date Posted | Impressions | Engagement | CTR | Notes |
|------|-------------|-------------|------------|-----|-------|
| Topic 1 - Post 1 | | | | | |
...

## Strategy Notes

- All posts follow LinkedIn best practices from workflows/linkedin-repurposing-guide.md
- Optimized for software developer audience
- Links placed in comments to maximize reach
- Hook-first approach for mobile feed visibility

## Next Steps

1. Review all posts in topic folders
2. Customize first comment with appropriate links
3. Schedule posts using preferred tool
4. Monitor engagement and adjust strategy
5. Respond to comments within 2 hours of posting
```

### Step 7: Validation and Quality Check

Before finalizing, verify each post:

**Content quality**:
- ✓ Hook is compelling and specific
- ✓ Value is clear in first 3 lines
- ✓ Targeted to software developers
- ✓ Actionable or thought-provoking
- ✓ No fluff or filler content

**Format quality**:
- ✓ Mobile-readable (short paragraphs)
- ✓ Visual variety (bullets, spacing)
- ✓ 300-500 words (optimal length)
- ✓ Conversational tone
- ✓ Engagement prompt included

**Technical quality**:
- ✓ No typos or grammar errors
- ✓ Proper use of technical terms
- ✓ Accurate information
- ✓ Hashtags relevant and not overdone (3-5 max)

## Examples

### Example 1: From AI Automation Video

**Input**: SRT file about automating tasks with AI
**Topics Extracted**:
1. Canvas feature for instant tool generation
2. Deep research vs regular chat
3. Integration with personal data (Gmail, Calendar)
4. Code execution for calculations
5. Tax simulator creation

**Sample Post (Topic 1 - Insight)**:
```
Most developers use ChatGPT for debugging.

They're missing 90% of its power.

I just watched someone build a working tax calculator in 3 minutes. Not code. An actual running tool.

Here's what most people don't know about AI canvas features:

→ Generates HTML/JS that runs immediately
→ Fixes its own bugs when you point them out
→ Creates UI without design skills
→ Exports working code you can deploy

The breakthrough? AI went from "help me code" to "here's your app."

The tools we use for chatting can build entire applications.

What's the most useful micro-tool you wish existed?

#SoftwareEngineering #AITools #ProductivityHacks
```

**First Comment**:
```
Full video breakdown of AI automation features: [YouTube URL]

I tested 5 different AI canvas tools - this one surprised me most.
```

### Example 2: From Career Development Video

**Topic**: Transitioning from developer to researcher
**Post Type**: Story

```
"Just move to Italy and do a PhD."

That was Eduardo's career advice to himself.

No safety net. No plan B. Just a belief that research > corporate development.

5 years later:
• Published in top-tier conferences
• Teaching next-gen developers
• Freedom to explore cutting-edge topics
• No more legacy code maintenance hell

But here's what he doesn't tell you upfront:

The transition from developer to researcher is brutal:
→ PhD salary = 60% pay cut
→ 3 years before first publication
→ Constant rejection of papers
→ Imposter syndrome x10

Was it worth it? He says absolutely.

The difference? His work creates knowledge instead of just features.

Would you trade salary for intellectual freedom?

#TechCareers #SoftwareEngineering #CareerDevelopment #Academia
```

## Input Parameters

- **video_dir** (required): Path to video directory (e.g., `25-12-05-kSdaDQh3TCw`)
- **srt_file** (optional): Specific SRT file path (auto-detected if not provided)
- **num_topics** (optional): Number of main topics to extract (default: 5)
- **posts_per_topic** (optional): Posts to generate per topic (default: 3-4)
- **tone** (optional): professional/conversational/technical/mix (default: conversational)
- **audience_focus** (optional): Specific developer niche (default: general software developers)

## Output Files

- **README.md**: Overview and posting schedule
- **topic-{n}-{slug}/post-{n}-{type}.md**: Individual post files
- **_strategy-approval.md**: Record of approved topics and approach

## Requirements

- **LinkedIn strategy guides**: workflows/linkedin-repurposing-guide.md
- **Example posts**: workflows/linkedin-posts-immigration-example.md
- **SRT file**: Valid subtitle file from YouTube
- **Understanding**: Deep knowledge of LinkedIn engagement patterns

## Best Practices

### Content Creation
- Extract real quotes/examples from video
- Use specific numbers and data
- Maintain speaker's voice/perspective
- Add relevant context for LinkedIn audience
- Make each post standalone (no "Part 1 of 3")

### LinkedIn Optimization
- Keep hook under 130 characters (mobile preview)
- Use line breaks every 1-2 sentences
- Place links in first comment, never main post
- Hashtags: 3-5 relevant, placed at end
- Tag people mentioned in video (with permission)

### Engagement Strategy
- End with questions, not statements
- Create debate with contrarian takes
- Share personal failures, not just wins
- Acknowledge different viewpoints
- Respond to comments promptly

### Posting Schedule
- **Best times**: 8 AM, 12 PM, 5 PM local time
- **Best days**: Tuesday-Thursday (highest engagement)
- **Frequency**: 2-3 posts per week (consistent > volume)
- **Spacing**: Minimum 48 hours between posts

## Advanced Features

### Topic Clustering
Group related subtopics for series:
- "3-part series on microservices"
- "This week: Career transition insights"

### A/B Testing
Create variations to test:
- Hook styles (question vs statement)
- Length (300 vs 500 words)
- Format (bullets vs paragraphs)

### Hashtag Strategy
- **Broad** (1-2): #SoftwareEngineering, #TechCareers
- **Specific** (2-3): #Microservices, #RemoteWork, #AITools
- **Trending** (0-1): Check LinkedIn trends

### Engagement Boosters
- Quote interesting commenters
- Create polls from post topics
- Share behind-the-scenes
- Acknowledge other thought leaders

## Common Pitfalls to Avoid

- ❌ Starting with "In this post, I'll discuss..."
- ❌ Using video thumbnail as post image (low engagement)
- ❌ Writing like a blog article
- ❌ Too many hashtags (looks spammy)
- ❌ Linking in main post (kills algorithmic reach)
- ❌ Being too salesy or promotional
- ❌ Ignoring comments
- ❌ Posting irregularly

## Success Metrics

Track these for each post:
- **Impressions**: Total views (goal: 2000+)
- **Engagement rate**: Comments+likes/impressions (goal: 5%+)
- **Comments**: Quality discussions (goal: 10+)
- **CTR**: Clicks to blog/video (goal: 2%+)
- **Follower growth**: New connections (goal: 5-10 per post)

## Notes

- Each video can generate 15-20 high-quality posts
- Posts should feel native to LinkedIn, not repurposed
- Quality > Quantity: Better to post 2 great posts than 5 mediocre
- Engagement in first 2 hours determines algorithmic distribution
- LinkedIn favors accounts that engage with others, not just post
- Document carousel posts get 3x more engagement than text-only
- Video clips (native to LinkedIn) get 5x more reach
- Consistency builds authority more than viral posts

## Future Enhancements

- Generate document carousel PDFs (10 slides per topic)
- Create short video clips for each topic
- Generate image quotes with text overlay
- Build thread versions for Twitter/X cross-posting
- Track successful posts for template refinement
- Analyze engagement patterns to optimize posting times
