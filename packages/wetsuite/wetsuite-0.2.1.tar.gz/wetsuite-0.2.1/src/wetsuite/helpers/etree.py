'''
Helpers to deal with XML data, largely a wrapper around lxml and its ElementTree interface.

TODO: minimize the amount of "will break because we use the lxml flavour of ElementTree",
and add tests for that.
    
Some general helpers.    
...including some helper functions shared by some debug scripts.

CONSIDER: 
  - A "turn tree into nested dicts" function - see e.g. https://lxml.de/FAQ.html#how-can-i-map-an-xml-tree-into-a-dict-of-dicts
  - have a fromstring() as a thin wrapper but with strip_namespace in there? (saves a lines but might be a confusing API change)
'''

import copy
import warnings

import lxml.etree
from lxml.etree import ElementTree, fromstring, tostring, register_namespace, Element, _Comment, _ProcessingInstruction #there is, and not actually (respectively), so  pylint: disable=E0611,W0611

SOME_NS_PREFIXES = { # CONSIDER: renaming to something like _some_ns_prefixes_presetation_only
    # Web and data
    'http://www.w3.org/2000/xmlns/':'xmlns',
    'http://www.w3.org/2001/XMLSchema':'xsd',

    # ?   Also, maybe avoid duplicate names? Except we are only doing this _only_ for pretty printing.
    #'http://www.w3.org/2001/XMLSchema#':'xsd',

    'http://www.w3.org/XML/1998/namespace':'xml',

    'http://www.w3.org/2001/XMLSchema-instance':'xsi',
    'http://www.w3.org/1999/xhtml':'xhtml',
    'http://www.w3.org/1999/xlink':'xlink',
    'http://schema.org/':'schema',
    'http://www.w3.org/2005/Atom':'atom',

    'http://www.w3.org/2000/svg':'svg',
    'http://www.w3.org/1998/Math/MathML':'mathml', # more usually m: or mml: but this may be clearer
    'http://www.w3.org/2001/XInclude':'xi',
    'http://www.w3.org/1999/XSL/Transform':'xsl', # there seem to be multiple. See also http://www.w3.org/XSL/Transform/1.0 and http://www.w3.org/TR/WD-xsl ?
    'http://www.w3.org/2005/xpath-functions#':'xpath-fn',
    #'http://icl.com/saxon':'saxon',
    #'http://xml.apache.org/xslt':'xalan',
    'http://www.w3.org/1999/XSL/Format':'fo',
    'http://www.w3.org/2003/g/data-view#':'grddl',
    'http://www.w3.org/2006/time#':'time',

    # getting into semantic data, linked data
    #cf dc, see also https://stackoverflow.com/questions/47519315/what-is-the-difference-between-dublin-core-terms-and-dublin-core-elements-vocabu
    'http://purl.org/dc/terms/':'dcterms', 
    'http://purl.org/dc/elements/1.1/':'dc',
    'http://purl.org/cld/freq/':'freq',

    'http://www.w3.org/1999/02/22-rdf-syntax-ns#':'rdf',
    'http://www.w3.org/2000/01/rdf-schema':'rdfs',
    'http://www.w3.org/2000/01/rdf-schema#':'rdfs',
    'http://www.w3.org/ns/rdfa#':'rdfa',
    'http://www.w3.org/TR/vocab-regorg/':'rov',
    'http://www.w3.org/TR/vocab-org/':'org',
    'http://www.w3.org/2004/02/skos/core#':'skos',
    'http://www.w3.org/TR/skos-reference/':'skosref',
    'http://www.w3.org/2008/05/skos-xl#':'skosxl',
    'http://www.w3.org/2002/07/owl#':'owl',

    'http://rdfs.org/ns/void#':'void', # Vocabulary of Interlinked Datasets 
    'http://purl.org/rss/1.0/modules/content/':'content',
    'http://purl.org/linked-data/version#':'version',
    'http://www.w3.org/ns/locn':'location',

    'http://xmlns.com/foaf/0.1/':'foaf',
    'http://ogp.me/ns#':'opengraph',
    'http://rdfs.org/sioc/ns#':'sioc',
    'http://rdfs.org/sioc/types#':'sioc-types',
    'http://purl.org/linked-data/registry#':'reg',
    'http://www.w3.org/ns/prov#':'prov',
    'http://purl.org/pav/':'pav',

    # Government
    'http://tuchtrecht.overheid.nl/':'tucht',
    'http://www.tweedekamer.nl/xsd/tkData/v1-0':'tk',
    'http://publications.europa.eu/celex/':'celex',
    'http://decentrale.regelgeving.overheid.nl/cvdr/':'cvdr',
    'http://psi.rechtspraak.nl/':'psi',
    'https://e-justice.europa.eu/ecli':'ecli',
    'http://www.rechtspraak.nl/schema/rechtspraak-1.0':'recht', # ?

    'http://standaarden.overheid.nl/owms/terms/':'overheid',
    'http://standaarden.overheid.nl/owms/terms':'overheid',  # maybe 'owms' would be clearer?
    'http://standaarden.overheid.nl/rijksoverheid/terms':'rijksoverheid',
    'http://standaarden.overheid.nl/inspectieloket/terms/':'inspectieloket',
    'http://standaarden.overheid.nl/buza/terms/':'overheid-buza',
    'http://standaarden.overheid.nl/oep/meta/':'overheid-oep', 
    'http://standaarden.overheid.nl/op/terms/':'overheid-op', 
    'http://standaarden.overheid.nl/product/terms/':'overheid-product',
    'http://standaarden.overheid.nl/cvdr/terms/':'overheid-rg', # decentrale regelgeving
    'http://standaarden.overheid.nl/vac/terms/':'overheid-vac', # ?vocabularies?
    'http://standaarden.overheid.nl/vb/terms/':'overheid-vastgoedbeheer',
    'http://standaarden.overheid.nl/bm/terms/':'overheid-bm',
    'http://standaarden.overheid.nl/vergunningen/terms/':'overheid-vergunning',

    'http://standaarden.overheid.nl/dcatnl/terms/':'dcatnl',
    'http://publications.europa.eu/resource/authority/file-type/':'file-type',
    'http://standaarden-acc.overheid.nl/owms/oquery/':'oquery',

    'https://identifier.overheid.nl/tooi/id/ministerie/':'ministerie',
    'https://identifier.overheid.nl/tooi/def/':'tooi',
    'https://identifier.overheid.nl/tooi/def/ont/':'tooiont',
    'https://identifier.overheid.nl/tooi/def/thes/top/':'tooitop',
    'https://identifier.overheid.nl/tooi/def/wl/':'tooiwl',

    # unsorted
    'http://spinrdf.org/sp#':'sparql-spin',
    'http://proton.semanticweb.org/2005/04/protons#':'protons',
    'http://purl.org/NET/scovo#':'scovo',  # Statistical Core Vocabulary?
    'http://rdf4j.org/schema/rdf4j#':'rdf4j',
    'http://www.openrdf.org/schema/sesame#':'sesame',
    'http://schemas.microsoft.com/ado/2007/08/dataservices':'ms-odata',
    'http://schemas.microsoft.com/ado/2007/08/dataservices/metadata':'ms-odata-meta',

    'www.kadaster.nl/schemas/lvbag/gem-wpl-rel/gwr-producten-lvc/v20200601':'bag',
    'www.kadaster.nl/schemas/lvbag/gem-wpl-rel/bag-types/v20200601':'bag-types',
    #'www.kadaster.nl/schemas/lvbag/gem-wpl-rel/gwr-deelbestand-lvc/v20200601':'bag-o',
    #'http://www.kadaster.nl/schemas/lvbag/extract-selecties/v20200601':'bag-s',
}
''' some readable XML prefixes, for friendlier display.  
    This is ONLY for consistent pretty-printing in debug,
    and will NOT be correct according to the document definition. '''
# It might be useful to find namespaces from many XML files, with something like:
#   locate .xml | tr '\n' '\0' | xargs -0 grep -oh 'xmlns:[^ >]*'
# with an eventual
#   | sort | uniq -c | sort -rn


def kvelements_to_dict(under_node, strip_text=True, ignore_tagnames=()) -> dict:
    ''' Where people use elements for single text values, it's convenient to get them as a dict.
        
        Given an etree element containing a series of such values,
        Returns a dict that is mostly just  { el.tag:el.text }  so ignores .tail
        Skips keys with empty values.
        
        Would for example turn an etree fragment like ::
            <foo>
                <identifier>BWBR0001840</identifier>
                <title>Grondwet</title>
                <onderwerp/>
            </foo>
        into python dict: ::
            {'identifier':'BWBR0001840', 'title':'Grondwet'}

        @param under_node: etree node/element to work under (use the children of)
        @param strip_text: whether to use strip() on text values (defaults to True)
        @param ignore_tagnames: sequence of strings, naming tags/variables to not put into the dict
        @return: a python dict (see e.g. example above)
    '''
    ret = {}
    for ch in under_node:
        if isinstance(ch, (_Comment, _ProcessingInstruction)):
            continue
        if ch.tag in ignore_tagnames:
            continue
        if ch.text is not None:
            text = ch.text
            if strip_text:
                text = text.strip()
            ret[ch.tag] = text
    return ret


def all_text_fragments(under_node, strip:str=None, ignore_empty:bool=False, ignore_tags=(), join:str=None, stop_at:list=None): # , add_spaces=['extref',]
    ''' Returns all fragments of text contained in a subtree, as a list of strings.

        For example,  all_text_fragments( fromstring('<a>foo<b>bar</b></a>') ) == ['foo', 'bar']

        Note that this is a convenience function that lets you be pragmatic with creative HTML-like nesting,
        and perhaps should not be used for things that are strictly data.

        @param strip: is what to remove at the edges of each .text and .tail 
        ...handed to strip(), and note that the default, None, is to strip whitespace
        if you want it to strip nothing at all, pass in '' (empty string)

        @param ignore_empty: removes strings that are empty when after that stripping

        @param ignore_tags: ignores direct/first .text content of named tags (does not ignore .tail, does not ignore the subtree)

        @param stop_at: should be None or a list of tag names. 
        If a tag name is in this sequence, we stop walking the tree entirely.
        (note that it would still include that tag's tail; CONSIDER: changing that)

                    
        TODO: more tests, I'm moderately sure strip doesn't do quite what it should.

        TODO: add_spaces - an acknowledgment that in non-HTML, 
        as well as equally free-form documents like this project often handles, 
        that element should be considered to split a word (e.g. p in HTML) or 
        that element probably doesn't split a word (e.g. em, sup in HTML)

        Here you specify the things where we add spaces (maybe prepend to .text and .tail).
        This is creative and not necessarily correct, but on average makes fewer weird mistakes
        TODO: figure out a decent default from the various schemas
    '''
    ret = []
    for elem in under_node.iter(): # walks the subtree
        if isinstance(elem, _Comment) or isinstance(elem, _ProcessingInstruction):
            continue
        #print("tag %r in ignore_tags (%r): %s"%(elem.tag, ignore_tags, elem.tag in ignore_tags))
        if elem.text is not None:
            if elem.tag not in ignore_tags: # only ignore contents of ignored tags; tail is considered outside
                etss = elem.text.strip(strip)
                if ignore_empty and len(etss)==0:
                    pass
                else:
                    ret.append( etss )
        if elem.tail is not None:
            etss = elem.tail.strip(strip)
            if ignore_empty and len(etss)==0:
                pass
            else:
                ret.append( etss )

        if stop_at is not None  and  elem.tag in stop_at:
            break

    if join is not None:
        ret = join.join( ret )
    return ret


def strip_namespace(tree, remove_from_attr=True):
    ''' Returns a copy of a tree that has its namespaces stripped.

        More specifically it removes
          - namespace from element names
          - namespaces from attribute names (default, but optional)
          - default namespaces (TODO: test that properly)

        
        @param tree:             The node under which to remove things 
        (you would probably hand in the root)
        @param remove_from_attr: Whether to remove namespaces from attributes as well.
        For attributes with the same name that are unique only because of a different namespace,
        this may cause attributes to be overwritten, For example:  ::
            <e p:at="bar" at="quu"/>   
        might become: ::
            <e at="bar"/>
        I've not yet seen any XML where this matters - but it might.        
        @return: The URLs for the stripped namespaces. 
        We don't expect you to have a use for this most of the time, 
        but in some debugging you want to know, and report them.                     
    '''
    if tree is None: # avoid the below saying something silly when it's you who were silly
        raise ValueError("Handed None to strip_namespace()")

    # make copy, an check it's of the right type
    if not isinstance(tree, lxml.etree._Element): #pylint: disable=W0212,I1101
        # we assume that means we're using a non-lxml etree  (and not that you handed in something completely unrelated)
        warnings.warn(
            "Trying to work around potential issues from non-lxml etrees by converting to it, which might be unnecessarily slow. "
            "If you parse your XML yourself, please consider lxml.etree.fromstring() / wetsuite.helpers.etree.fromstring() instead of e.g. xml.etree.fromstring()."
        )
        try:
            import xml.etree.ElementTree
            if isinstance(tree, xml.etree.ElementTree.Element):
                # We want a copy anyway, so this isn't too wasteful.   Maybe there is a faster way, though.
                tree = lxml.etree.fromstring( xml.etree.ElementTree.tostring( tree ) )
            #implied else: we don't know what that was, and we hope for the best
        except ImportError:
            pass # xml.etree is stdlib in py3 so this should never happen, but we can fall back to do nothing
    else:
        tree = copy.deepcopy( tree ) # assuming this is enough.  TODO: verify with lxml and etree implementation

    _strip_namespace_inplace(tree, remove_from_attr=remove_from_attr)
    return tree


def _strip_namespace_inplace(tree, remove_from_attr=True):
    ''' Takes a parsed ET structure and does an in-place removal of all namespaces.
        Returns a list of removed namespaces, which you can usually ignore.
        Not really meant to be used directly, in part because it assumes lxml etrees.

        @param tree:             See L{strip_namespace}
        @param remove_from_attr: See L{strip_namespace}
        @return:                 See L{strip_namespace}
    '''
    ret = {}
    for elem in tree.iter():
        if isinstance(elem, _Comment): # won't have a .tag to have a namespace in,
            continue # so we can ignore it
        if isinstance(elem, _ProcessingInstruction): # won't have a .tag to have a namespace in,
            continue # so we can ignore it
        tagname = elem.tag
        if tagname[0]=='{':
            elem.tag = tagname[ tagname.index('}',1)+1: ]
        if remove_from_attr:
            to_delete = []
            to_set    = {}
            for attr_name in elem.attrib:
                if attr_name[0]=='{':
                    urlendind = attr_name.index('}', 1)
                    ret[ attr_name[1:urlendind] ] = True
                    old_val = elem.attrib[attr_name]
                    to_delete.append( attr_name )
                    attr_name = attr_name[urlendind+1:]
                    to_set[attr_name] = old_val
            for delete_key in to_delete:
                elem.attrib.pop( delete_key )
            elem.attrib.update( to_set )
    lxml.etree.cleanup_namespaces( tree ) # remove unused namespace declarations. Will only work on lxml etree objects, hence the code above.
    return ret


def indent(tree, strip_whitespace:bool=True):
    ''' Returns a 'reindented' copy of a tree,
        with text nodes altered to add spaces and newlines, so that it would print indented by depth.

        Keep in mind that this may change the meaning of the document,
        so this output should _only_ be used for presentation of the debugging sort.

        See also L{_indent_inplace}
        @param tree:             tree to copy and reindent
        @param strip_whitespace: make contents that contain a lot of newlines look cleaner, but changes the stored data even more.
    '''
    newtree = copy.deepcopy( tree )
    _indent_inplace(newtree, level=0, strip_whitepsace=strip_whitespace)
    return newtree


def _indent_inplace(elem, level:int=0, strip_whitepsace:bool=True):
    ''' Alters the text nodes so that the tostring()ed version will look nice and indented when printed as plain text.
    '''
    i = "\n" + level*"  "

    if strip_whitepsace:
        if elem.text:
            elem.text=elem.text.strip()
        if elem.tail:
            elem.tail=elem.tail.strip()

    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            _indent_inplace(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def path_between(under_node, element, excluding:bool=False):
    ''' Given an ancestor and a descentent element from the same tree
        (In many applications you want under to be the the root element)

        Returns the xpath-style path to get from (under) to this specific element
        ...or raises a ValueError mentioning that the element is not in this tree

        Keep in mind that if you reformat a tree, the latter is likely.

        This function has very little code, and if you do this for much of a document, you may want to steal the code
        
        @param excluding: if we have   a/b/c  and call this between an and c, there are cases for wanting either
          * complete path report, like `/a/b/c` (excluding=False), e.g. as a 'complete
          * a relative path like `b/c` (excluding=True), in particular when we know we'll be calling xpath or find on node a
        @param under_node: 
        @param element: 
        @return: 
    '''
    if excluding is False:
        letree = lxml.etree.ElementTree( under_node ) # it does, actually, so pylint: disable=I1101
        return letree.getpath( element )
    else:
        letree = lxml.etree.ElementTree( under_node ) # it does, actually, so pylint: disable=I1101
        path = letree.getpath( element )
        path = path[path.find('/',1)+1:]
        return path

def node_walk(under_node, max_depth=None):
    ''' Walks all elements under the given element,
        remembering both path string and element reference as we go.
        
        (note that this is not an xpath style with specific indices, just the names of the elements)

        For example: ::
            TODO

        TODO: re-test now that I've added max_depth, because I'm not 100% on the details

        @param under_node: If given None, it emits nothing 
        (we assume it's from a find() that hit nothing, and that it's slightly easier to ignore here than in your code)
        @param max_depth: 
        @return:             a generator yielding (path, element),   and is mainly a helper used by path_count()
    '''
    # Based on https://stackoverflow.com/questions/60863411/find-path-to-the-node-using-elementtree
    if under_node is None:
        return
    path_to_element = []
    element_stack = [under_node]
    while len(element_stack) > 0:
        element = element_stack[-1]
        if len(path_to_element) > 0  and  element is path_to_element[-1]:
            path_to_element.pop()
            element_stack.pop()
            yield (path_to_element, element)
        else:
            path_to_element.append( element )
            for child in reversed( element ):
                if max_depth is None or (max_depth is not None and len(path_to_element) < max_depth):
                    element_stack.append( child )


def path_count(under_node, max_depth=None):
    ''' Walk nodes under an etree element,
        count how often each path happens (counting the complete path string).
        written to summarize the rough structure of a document.

        Path here means 'the name of each element', 
        *not* xpath-style path with indices that resolve to the specific node.

        Returns a dict from each path strings to how often it occurs
    '''
    count = {}
    for node_path, n in node_walk( under_node, max_depth=max_depth ):
        if isinstance(n, (_Comment, _ProcessingInstruction)):
            continue # ignore things that won't have a .tag
        path = "/".join([n.tag  for n in node_path] + [n.tag] )  # includes `under`` element, which is a little redundant, but more consistent
        if path not in count:
            count[ path ]  = 1
        else:
            count[ path ] += 1
    return count



def debug_pretty(tree, reindent=True, strip_namespaces=True, encoding='unicode'):
    ''' Return (piece of) tree as a string, readable for debugging

        Intended to take an etree object  (but if give a bytestring we'll try to parse it as XML)
        
        Because this is purely meant for debugging, it by default
          - strips namespaces
          - reindents
          - returns as unicode (not bytes) so we can print() it

        It's also mostly just short for::
               etree.tostring(  etree.indent( etree.strip_namespace( tree ) ), encoding='unicode' )
    '''
    if tree is None:
        raise ValueError("Handed None to debug_pretty()")

    if isinstance(tree, bytes): # if you gave it an unparsed doc instead (as bytes, not str)
        tree = lxml.etree.fromstring( tree )

    if strip_namespaces:
        tree = strip_namespace( tree )

    if reindent:
        tree = indent( tree )

    return tostring( tree, encoding=encoding )



class debug_color():
    ''' Takes XML, 
        - applies debug_pretty 
        - returns a class that will renderer it in color in a jupyter notebook.
    
        relies on pygments; CONSIDER: removing that dependency,
        we already have much of the code in the xml-color tool
    '''
    def __init__(self, tree_or_bytestring):
        self.xstr = debug_pretty( tree_or_bytestring )
        #if isinstance(tree_or_bytestring, (str, bytes)):
        #    self.xstr = tree_or_bytestring # TODO: ensure bytes?
        #else:
        #    self.xstr = tostring( tree_or_bytestring, encoding='utf-8' )

    def _repr_html_(self):
        #try:
        from pygments.lexers.html import XmlLexer
        from pygments.formatters import HtmlFormatter
        from pygments import highlight
        html = highlight( self.xstr, XmlLexer(), HtmlFormatter())
        return '<style>%s%s</style>%s'%(
            HtmlFormatter().get_style_defs('.highlight'),
            '\n* { background-color: transparent !important; color:inherit };',  # TODO: consider a light and dark mode
            html
        )
        #except ImportError:
        #    fall back to escaped
        #    return escape.  xstr
