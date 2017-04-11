<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="text" encoding="utf-8"/>
  <xsl:strip-space elements="*"/>
  <xsl:key name="senses" match="/rwn/senses/sense" use="@synset_id"/>
  <xsl:template match="/">
    <xsl:for-each select="/rwn/relations/relation[@name='hypernym']">
      <xsl:call-template name="relations">
        <xsl:with-param name="from" select="@parent_id"/>
        <xsl:with-param name="to"   select="@child_id"/>
      </xsl:call-template>
    </xsl:for-each>
    <xsl:for-each select="/rwn/relations/relation[@name='hyponym']">
      <xsl:call-template name="relations">
        <xsl:with-param name="from" select="@child_id"/>
        <xsl:with-param name="to"   select="@parent_id"/>
      </xsl:call-template>
    </xsl:for-each>
  </xsl:template>
  <xsl:template name="relations">
    <xsl:param name="from"/>
    <xsl:param name="to"/>
    <xsl:for-each select="key('senses', $from)">
      <xsl:variable name="x" select="@name"/>
      <xsl:for-each select="key('senses', $to)">
        <xsl:variable name="y" select="@name"/>
        <!-- from#sid -->
        <xsl:value-of select="$x"/>
        <xsl:text>#</xsl:text>
        <xsl:value-of select="$from"/>
        <xsl:text>&#9;</xsl:text>
        <!-- to#sid -->
        <xsl:value-of select="$y"/>
        <xsl:text>#</xsl:text>
        <xsl:value-of select="$to"/>
        <xsl:text>&#10;</xsl:text>
      </xsl:for-each>
    </xsl:for-each>
  </xsl:template>
</xsl:stylesheet>
