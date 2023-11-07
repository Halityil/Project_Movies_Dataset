#!/usr/bin/env python
# coding: utf-8

# </strong>Explanatory Data Analysis & Data Presentation Using Movies Dataset</strong>

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
pd.options.display.max_columns = 30
pd.options.display.float_format = '{:.2f}'.format


# In[2]:


df = pd.read_csv("movies_complete.csv", parse_dates =["release_date"])


# In[3]:


df


# In[4]:


df.info()


# In[5]:


df.genres[1]


# In[6]:


df.cast[1]


# In[7]:


df.describe()


# In[8]:


df.hist(figsize = (20, 12), bins=100)
plt.show()


# In[9]:


df.budget_musd.value_counts(dropna = False).head(20)


# In[10]:


df.revenue_musd.value_counts(dropna = False).head(20)


# In[11]:


df.vote_average.value_counts()


# In[12]:


df.vote_count.value_counts()


# In[13]:


df.describe(include = "object")


# In[14]:


df[df.title=="Cinderella"]


# In[15]:


from IPython.display import HTML


# In[16]:


df_best = df[["poster_path","title","budget_musd", "revenue_musd","vote_count", "vote_average","popularity"]].copy()


# In[17]:


df_best


# In[18]:


df_best["profit_musd"] = df.revenue_musd.sub(df.budget_musd)
df_best["return"] = df.revenue_musd.div(df.budget_musd)


# In[19]:


df_best


# In[20]:


df_best.columns=[" ","Title","Budget","Revenue","Votes","Average Rating","Popularity", "Profit", "ROI"]


# In[21]:


df_best.set_index("Title", inplace = True)


# In[22]:


df_best


# In[23]:


df_best.iloc[0,0]


# In[24]:


subset = df_best.iloc[:5, :2]
subset


# In[25]:


HTML(subset.to_html(escape=False))


# In[26]:


df_best.sort_values(by = "Average Rating", ascending = False)


# In[27]:


df_best.sort_values(by = "ROI", ascending = False)


# In[28]:


df_best.loc[df_best.Budget >= 5].sort_values(by = "ROI", ascending = False)


# In[29]:


df_best.Budget.fillna(0, inplace = True)
df_best.Votes.fillna(0, inplace = True)


# In[30]:


df_best.info()


# In[31]:


def best_worst(n, by, ascending = False, min_bud = 0, min_votes = 0):
    
    df2 = df_best.loc[(df_best.Budget >= min_bud) & (df_best.Votes >= min_votes),[" ",by]].sort_values(by = by, ascending = ascending).head(n).copy()
    
    return HTML(df2.to_html(escape=False))


# Movies Top 5 - Highest Revenue
# 

# In[32]:


best_worst(n = 5, by = "Revenue")


# Movies Top 5 - Highest Profit

# In[33]:


best_worst(5, "Profit")


# Movies Top 5 - Highest Budget

# In[34]:


best_worst(5, "Budget")


# Movies Top 5 - Lowest Profit

# In[35]:


best_worst(5, "Profit", ascending = True)


# Movies Top 5 - Highest ROI

# In[36]:


best_worst(5, "ROI", min_bud = 0)


# Moviest Top 5 - Lowest ROI

# In[37]:


best_worst(5, "ROI", ascending = True, min_bud = 1)


# Moviest Top 5 - Most Votes

# In[38]:


best_worst(5, "Votes")


# Movies Top 5 - Highest Rating

# In[39]:


best_worst(5, "Average Rating", min_votes = 100)


# Movies Top 5 - Lowest Rating

# In[40]:


best_worst(5, "Average Rating", ascending = True, min_votes = 100)


# Movies Top 5 - Popularity

# In[41]:


best_worst(5, "Popularity")


# Find your next movie

# Search 1: Sciene Fiction Action Movie with Bruce Willis (High Rating)

# In[42]:


df.genres[0]


# In[43]:


mask_genres = df.genres.str.contains("Action") & df.genres.str.contains("Science Fiction")
mask_genres


# In[44]:


df.cast[0]


# In[45]:


mask_actor = df.cast.str.contains("Bruce Willis")
mask_actor


# In[46]:


df.loc[mask_actor & mask_genres, ["title", "vote_average"]].sort_values(by = "vote_average", ascending = False)


# In[47]:


bruce = df.loc[mask_actor & mask_genres, ["title","poster_path", "vote_average"]].sort_values(by = "vote_average", ascending = False)
HTML(bruce.to_html(escape=False))


# Search 2: Movies with Uma Thurman and directred by Quentin Tarantino (low runtime)

# In[48]:


df.director


# In[49]:


mask_director = df.director == "Quentin Tarantino"


# In[50]:


mask_actor = df.cast.str.contains("Uma Thurman")


# In[51]:


quentin = df.loc[mask_director & mask_actor, ["title", "poster_path", "runtime"]].sort_values(by = "runtime").set_index("title")


# In[52]:


HTML(quentin.to_html(escape=False))


# Search 3: Most Successful Pixar Studio Movies between 2010 and 2015 (High Revenue)

# In[53]:


df.production_companies[1]


# In[54]:


mask_studio = df.production_companies.str.contains("Pixar").fillna(False)


# In[55]:


df.release_date


# In[56]:


mask_time = df.release_date.between("2010-01-01", "2015-12-31")


# In[57]:


pixar = df.loc[mask_studio & mask_time, ["title", "poster_path", "revenue_musd", "release_date"]].sort_values(by = "revenue_musd").set_index("title")


# In[58]:


HTML(pixar.to_html(escape=False))


# In[59]:


from wordcloud import WordCloud


# In[60]:


df


# In[61]:


df.tagline[1]


# In[62]:


df.overview[1]


# In[63]:


title = df.title.dropna()
overview = df.overview.dropna()
tagline = df.tagline.dropna()


# In[64]:


title


# In[65]:


''.join(title)


# In[66]:


title_corpus = ' '.join(title)
overview_corpus = ' '.join(overview)
tagline_corpus = ' '.join(tagline)


# In[67]:


tagline_corpus


# In[68]:


title_wordcloud = WordCloud(background_color='white', height=2000, width=4000, max_words= 200).generate(title_corpus)
title_wordcloud


# In[69]:


plt.figure(figsize=(16,8))
plt.imshow(title_wordcloud, interpolation="bilinear")
plt.axis('off')
plt.show()


# In[70]:


tagline_wordcloud = WordCloud(background_color='white', height=2000, width=4000, max_words= 200).generate(tagline_corpus)
plt.figure(figsize=(16,8))
plt.imshow(tagline_wordcloud, interpolation="bilinear")
plt.axis('off')
plt.show()


# Are Franchises more succesfful?

# In[71]:


df.belongs_to_collection


# In[72]:


df["Franchise"] = df.belongs_to_collection.notna()


# In[73]:


df.Franchise


# In[74]:


df.Franchise.value_counts()


# Franchise vs Stand-alone:Average Revenue

# In[75]:


df.groupby("Franchise").revenue_musd.mean()


# Franchise vs Stand-alone:Return on Investment / Profitability

# In[76]:


df['ROI'] = df.revenue_musd.div(df.budget_musd)


# In[77]:


df.groupby('Franchise').ROI.median()


# Franchise vs Stand-alone:Average Budget

# In[78]:


df.groupby("Franchise").budget_musd.mean()


# Most Successful Franchises

# In[79]:


df.belongs_to_collection


# In[80]:


df.belongs_to_collection.value_counts()


# In[81]:


franchises = df.groupby("belongs_to_collection").agg({"title":"count", "budget_musd": ["sum", "mean"],
                                                     "revenue_musd": ["sum", "mean"],
                                                     "vote_average": "mean", "popularity": "mean",
                                                     "ROI":"median",
                                                     "vote_count":"mean"})


# In[82]:


franchises


# In[83]:


franchises.nlargest(20, ("title", "count"))


# In[84]:


franchises.nlargest(20, ("revenue_musd", "sum"))


# In[85]:


franchises.nlargest(20, ("revenue_musd", "mean"))


# In[86]:


franchises.nlargest(20, ("budget_musd", "sum"))


# In[87]:


franchises[franchises[("vote_count", "mean")] >=1000].nlargest(20, ("vote_average", "mean"))


# In[88]:


df.director


# In[89]:


df.director.value_counts().head(20)


# In[90]:


plt.figure(figsize = (12,8))
df.director.value_counts().head(20).plot(kind='bar', fontsize = 15)
plt.title("Most Active Directors", fontsize = 20)
plt.ylabel("Number of Movies", fontsize = 15)
plt.show()


# In[91]:


df.groupby("director").revenue_musd.sum().nlargest(20)


# In[92]:


plt.figure(figsize = (12,8))
df.groupby("director").revenue_musd.sum().nlargest(20).plot(kind='bar', fontsize = 15)
plt.title("Total Revenue", fontsize = 20)
plt.ylabel("Revenue (in MUSD)", fontsize = 15)
plt.show()


# In[93]:


directors = df.groupby("director").agg({"title": "count", "vote_average" :"mean", "vote_count": "sum"})


# In[94]:


directors


# In[95]:


directors[(directors.vote_count >= 10000) & (directors.title >= 10)].nlargest(20, "vote_average")


# In[96]:


df.genres = df.genres.astype(str)


# In[97]:


df.loc[df.genres.str.contains("Horror")].groupby("director").revenue_musd.sum().nlargest(20)


# Most Successful Actors

# In[98]:


df.cast


# In[99]:


df.set_index("id", inplace = True)


# In[100]:


df.info()


# In[102]:


df.cast


# In[104]:


df.cast.str.split("|", expand = True)


# In[105]:


act = df.cast.str.split("|", expand = True)
act


# In[114]:


act = act.stack().reset_index(level = 1, drop=True).to_frame()


# In[115]:


act.columns = ["Actor"]


# In[116]:


act


# In[117]:


act = act.merge(df[["title", "revenue_musd", "vote_average", "popularity"]],
               how = "left", left_index = True, right_index = True)


# In[118]:


act


# In[119]:


act.Actor.nunique()


# In[120]:


act.Actor.unique()


# In[121]:


act.Actor.value_counts().head(20)


# In[123]:


plt.figure(figsize = (12,8))
act.Actor.value_counts().head(20).plot(kind="bar", fontsize = 15)
plt.title("Most Active Actors", fontsize = 20)
plt.ylabel("Number of Movies", fontsize = 15)
plt.show()


# In[124]:


agg = act.groupby("Actor").agg(Total_Revenue = ("revenue_musd", "sum"),
                               Mean_Revenue = ("revenue_musd", "mean"),
                               Mean_Rating = ("vote_average", "mean"),
                               Mean_Pop = ("popularity", "mean"),
                               Total_Movies = ("Actor", "count"))


# In[125]:


agg.nlargest(10, "Total_Movies")


# In[126]:


agg.nlargest(10, "Total_Revenue")


# In[127]:


plt.figure(figsize = (12,8))
agg.Total_Revenue.nlargest(10).plot(kind='bar', fontsize = 15)
plt.title("Total Revenue", fontsize = 20)
plt.ylabel("Revenue (in MUSD)", fontsize = 15)
plt.show()


# In[128]:


agg.Mean_Revenue.nlargest(10)


# In[130]:


act[act.Actor == "Tom Hardy"]


# In[131]:


agg[agg.Total_Movies >= 10].nlargest(10, "Mean_Revenue")


# In[132]:


agg[agg.Total_Movies >= 10].nlargest(10, "Mean_Rating")


# In[133]:


agg[agg.Total_Movies >= 10].nlargest(10, "Mean_Pop")


# In[ ]:




