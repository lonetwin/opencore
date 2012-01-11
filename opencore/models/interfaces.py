# Copyright (C) 2008-2009 Open Society Institute
#               Thomas Moroz: tmoroz.org
#               2010-2011 Large Blue
#               Fergus Doyle: fergus.doyle@largeblue.com
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License Version 2 as published
# by the Free Software Foundation.  You may not use, modify or distribute
# this program under any other version of the GNU General Public License.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

from zope.interface import Attribute
from zope.interface import Interface
from zope.interface import taggedValue

from repoze.folder.interfaces import IFolder
from repoze.lemonade.interfaces import IContent
from zope.component.interfaces import IObjectEvent

class ISite(IFolder):
    """ Karl site """
    taggedValue('name', 'Site')

    def update_indexes():
        """Add and remove catalog indexes to match a fixed schema"""


## Event interfaces ##
class IObjectWillBeModifiedEvent(IObjectEvent):
    """ An event type sent before an object is modified  """
    object = Attribute('The object that will be modified')

class IObjectModifiedEvent(IObjectEvent):
    """ An event type sent after an object is modified """
    object = Attribute('The object which was modified')

## end Event interfaces ##

class IRatingsFolder(IFolder):
    pass

class IRatable(Interface):
    pass

class IRatingUtility(Interface):
    
    def rate(creator, value, request):
        """Rate the object"""

class IFlagsFolder(IFolder):
    pass

class IFlag(IFolder):
    creator = Attribute(u'User ID of the creator')

class IFlaggable(Interface):
    pass

class IFlaggingUtility(Interface):
    
    def flag(user):
        """Flag the object"""
    
    def unflag(user):
        """Unflag the object"""
    
    def clear():
        """Clear all flags"""

class ICommunityContent(IContent):
    """ Base interface for content which is within a community.
    """
    creator = Attribute(u'Creating userid')
    modified_by = Attribute(u'ID of user who last modified the object')
    title = Attribute(u'Title of content')

# Interfaces for the LiveSearch grouping
class IPeople(Interface):
    """Grouping for LiveSearch and other purposes"""
    taggedValue('name', 'People')

class IOthers(Interface):
    """Grouping for LiveSearch and other purposes"""
    taggedValue('name', 'Others')

class IGroupSearchFactory(Interface):
    def __call__(context, request, term):
        """ return an object implementing IGroupSearch or None if
        no IGroupSearch can be found """




class IPosts(Interface):
    """Grouping for LiveSearch and other purposes"""
    taggedValue('name', 'Posts')

class ICommunity(IFolder, IContent, IOthers):
    """ Community folder """
    taggedValue('name', 'Community')
    taggedValue('search_option', True)

    description = Attribute(u'Description -- plain text summary')
    text = Attribute(u'Text -- includes wiki markup.')
    content_modified = Attribute(
        u'datetime: last modification to any subcontent ')

    members_group_name = Attribute(u'The group users belonging to this community belong to')
    moderators_group_name = Attribute(u'The group moderators of this community belong to')
    
    member_names = Attribute(u'The usernames of community members')
    moderator_names = Attribute(u'The usernames of community moderators')
    
    number_of_members = Attribute(u'Number of community members')


class ICommunityInfo(Interface):
    """ An adapter for obtaining information about a single community
    """
    name = Attribute('The name of the community')
    title = Attribute('The title of the community')
    description = Attribute('The description of the community')
    url = Attribute("Community URL")
    number_of_members = Attribute("Number of members in the community")
    last_activity_date = Attribute("Date content was last modified")


class IFiles(Interface):
    """Grouping for LiveSearch and other purposes"""
    taggedValue('name', 'Files')


# --- end LiveSearch grouping

class IIndexFactory(Interface):
    """ Register as named utilities to add extra indexes to the catalog.
    """
    def __call__():
        """ Return an index.

        The index will be added to the catalog under the name of the utility.
        """


class ITempFolder(IFolder):
    """ A container for temporary storage of documents. """

    def add_document(doc):
        """
        Adds a document to the temporary folder, assigning a unique identifier.
        """

    def cleanup():
        """
        Removes 'old' documents from the folder.
        """

class ICommunities(IFolder):
    """ Communities folder """
    taggedValue('name', 'Communities')

class ICommentsFolder(IFolder):
    """ A container for comments """
    taggedValue('name', 'Comments Folder')

class IComment(IFolder, ICommunityContent, IPosts):
    """ A container holding a comment and any attachments """
    taggedValue('name', 'Comment')
    taggedValue('search_option', True)

class IAttachmentsFolder(IFolder):
    """ A container for attachments (implemented as File objects) """
    taggedValue('name', 'Attachments Folder')

class IMembers(IFolder):
    """ Easy access to community member data, and store invitations"""
    taggedValue('name', 'Members')

class IInvitation(Interface):
    """ Persistent object with information for joining """
    taggedValue('name', 'Invitation')

    email = Attribute(u'Email address for the person being invited')
    message = Attribute(u'Personal message sent along with the invitation')

class IFeedsContainer(IFolder):
    """ Container for fetched feeds """
    taggedValue('name', 'Feeds')

class IFeed(IContent):
    taggedValue('name', 'Feed')

    title = Attribute('Title')
    subtitle = Attribute('Subtitle')
    link = Attribute('Link to source HTML page')

    etag = Attribute('Etag (bandwidth optimization)')
    feed_modified = Attribute('Last-modified date (bandwidth optimization)')

    entries = Attribute('List of contained IFeedEntry objects')

    old_uri = Attribute('Old feed URI (set if the feed moves or disappears)')
    new_uri = Attribute('New feed URI (set if the feed moves or disappears)')

    def update(parser):
        """Change the content to match a FeedParser result.
        """

class IFeedEntry(Interface):
    taggedValue('name', 'Feed Entry')

    title = Attribute('Title')
    summary = Attribute('Summary')
    link = Attribute('Link to source HTML page')
    id = Attribute('Globally unique entry identifier')
    content_html = Attribute('The content as a sanitized HTML string')
    published = Attribute('Publication date as a datetime')
    updated = Attribute('Last update as a datetime')

    def update(parser_entry):
        """Change the content to match a FeedParser entry.
        """

class IGallery(IFolder):
    taggedValue('name', 'Challenge Folder')

class IGalleryRenderable(Interface):
    """ Marker interface for content able to be rendered into the gallery widget
    """

class IGalleryContentRenderer(Interface):
    def __call__(request):
        """ Returns a 2-pair tuple in the form (html_markup, thumbnail_url)
        """
        
class IFiles(Interface):
    """Grouping for LiveSearch and other purposes"""
    taggedValue('name', 'Files')

class IFile(Interface):
    """ A model object which provides a file-like interface analogous to
        static resource.
    """
    stream = Attribute(u'A read-only stream for getting file contents.')
    mimetype = Attribute(u'Mime type of file')
    size = Attribute(u'Size in bytes of file')

class IImageFile(IFile):
    """ An image file.
    """
    extension = Attribute(u'File extension based on mime type')

class ICommunityFile(ICommunityContent, IFiles):
    """A file in a community"""
    taggedValue('name', 'File')
    taggedValue('search_option', True)

    blobfile = Attribute(u'Optional file attachment')
    mimetype = Attribute(u'Content type')
    filename = Attribute(u'Uploaded filename')
    size = Attribute(u'Size in bytes')

class ICommunityImage(IImageFile, ICommunityContent, IFiles, IGalleryRenderable):
    taggedValue('name', 'Image')


class IProfiles(IFolder):
    """ Profiles folder """
    taggedValue('name', 'Profiles')

    def getProfileByEmail(email):
        """ Return the profile which has the given email address.

        o Return None if no match is found.
        """

class IProfile(IFolder, IContent, IPeople):
    """ User profile """
    taggedValue('name', 'Profile')

    firstname = Attribute(u"User's first name.")
    lastname = Attribute(u"User's last name.")
    email = Attribute(u"User's email address.")
    
    description = Attribute(u"A motto or description")
    twitter = Attribute(u"User's twitter username")
    facebook = Attribute(u"Link to user's Facebook page")
    gender = Attribute(u"Gender of user")
    dob = Attribute(u"date of birth")
    
    # XXX The fields below (phone through biography) are OSI specific
    # and probably should be removed from here.  It's possible that
    # they don't need to be documented as interface attributes at all.
    phone = Attribute(u"User's phone number.")
    extension = Attribute(u"User's phone extension.")

    # XXX redundant with categories?
    department = Attribute(u"User's department.")

    position = Attribute(u"User's position.")

    # XXX redundant with categories?
    organization = Attribute(u"User's organization")

    location = Attribute(u"User's location.")
    country = Attribute(u"User's country.")
    website = Attribute(u"User's websites urls.")
    languages = Attribute(u"User's spoken languages.")

    # XXX redundant with categories?
    office = Attribute(u"User's office.")

    room_no = Attribute(u"User's room number.")
    biography = Attribute(u"User's biography.")

    home_path = Attribute(u"Path to user's home model, possibly including "
                          u"view.  May be None.")
    categories = Attribute(
        u"A dictionary that maps category key to a list of "
        u"category value identifier strings. "
        u"Example: {'departments': ['finance']}. "
        u"Typical keys: 'entities', 'offices', 'departments', 'other'")

    password_reset_key = Attribute(
        u"Key for confirming password reset.  "
        u"Not for display or editing.")
    password_reset_time = Attribute(
        u"Datetime when password reset was requested.  "
        u"Not for display or editing.")

    def get_alerts_preference(community_name):
        """Returns constant value representing user's alert preference for
        the given community.

        Possible values are:

        o IProfile.ALERT_IMMEDIATELY
        o IProfile.ALERT_DIGEST
        o IProfile.ALERT_NEVER

        """

    def set_alerts_preference(community_name, preference):
        """Sets user's alert preference for the given community.

        Possible values are:

        o IProfile.ALERT_IMMEDIATELY
        o IProfile.ALERT_DIGEST
        o IProfile.ALERT_NEVER

        """

# alerting bit flags 
IProfile.ALERT_EMAIL_IMMEDIATELY = 1
IProfile.ALERT_EMAIL_DIGEST = 2
IProfile.ALERT_EMAIL_NEVER = 4
IProfile.ALERT_INBOX = 8


class ITextContent(ICommunityContent, IFiles, IGalleryRenderable):
    """ Text based content
    """
    taggedValue('name', 'Text Content')
    taggedValue('search_option', True)    
    snippet = Attribute(u'Text to be displayed in listings')
    text = Attribute(u'Full text')

class ICreatedModified(Interface):
    """ Interface indicating content that has its created and modified
    attributes managed by an event subscriber (this implies all IContent
    content at the moment). """
    modified = Attribute(u'Datetime indicating modification')
    created = Attribute(u'Datetime indicating creation')

class IToolFactory(Interface):
    """ A utility interface """
    interfaces = Attribute(
        'Sequence of interface objects that inform ``is_current``. '
        'The context must be one of these for the tool factory to be '
        'considered "current" by the UI')

    name = Attribute('The tool factory name')

    def add(context, request):
        """ Perform the work required to add a tool """

    def remove(context, request):
        """ Perform the work required to remove a tool """

    def is_present(context, request):
        """ Return true if the tool is present in the context """

    def is_current(context, request):
        """ Returns true if the tool is the ``current`` tool """

    def tab_url(context, request):
        """ Returns the tab URL for the tool """

class ITextIndexData(Interface):
    """ An adapter which returns a string representing data useable
    for text indexing"""
    def __call__():
        """ Return text data """

class IVirtualData(Interface):
    """ An adapter which returns a hashable object representing
    'virtual' data for an object.  It's initial use is for the
    calendar category name/path associated with an ICalendarEvent, but
    content type adapters for cataloging should feel free to use it
    any time they need some adhoc identifying data about a piece of
    content as an extra filter argument."""
    def __call__():
        """ Return hashable data """

class ITokenManager(Interface):
    def get_new_token(key, expires):
        """ Returns a new token string """

    def expire_key(key):
        """ Expires the entry specified by `key`"""

    def expire_token(token):
        """ Expires the entry which has the specified `token` """
        
    def validate_key(key):
        """ Validates the entry specified by `key` and expires it if `token`
        was created with `expiry == 'TokenManager.ON_VALIDATION'`
        """

    def validate_token(token):
        """ Validates the entry specified by `token` and expires it if `token`
        was created with `expiry == 'TokenManager.ON_VALIDATION'`
        """

    def get_by_token(token):
        """ Returns the key which has the specified `token`
        """

class IStatusUpdateContainer(Interface):
    updates = Attribute(u'A list of StatusUpdate objects')

class IStatusUpdate(Interface):
    creator = Attribute(u'User ID of the creator')
    text = Attribute(u'Content of the status update')

class ICommentable(Interface):
    pass

class ICommentUtility(Interface):
    
    def addComment(text, creator, request):
        """Add a comment to the object"""
    
# XXX Arguably, this is display logic and belongs in views.
class IGridEntryInfo(Interface):
    """Adapt resources for display in a grid listing"""

    title = Attribute("")
    url = Attribute("")
    type = Attribute("")
    modified = Attribute("")
    created = Attribute("")
    creator_title = Attribute("")
    creator_url = Attribute("")
    modified_by_title = Attribute("")
    modified_by_url = Attribute("")

class ICommunityInfo(Interface):
    """ An adapter for obtaining information about a single community """
    name = Attribute('The name of the community')
    title = Attribute('The title of the community')
    description = Attribute('The description of the community')
    tags = Attribute("Tags applied to the community")
    number_of_members = Attribute("Number of members in the community")
    url = Attribute("Community URL")
    last_activity_date = Attribute("Date content was last modified")
    tabs = Attribute("Information on tabs available for the community view")
    community_tags = Attribute("Tags most used in the community")
    member = Attribute("Is the current user a member of the community?")
    moderator = Attribute("Is the current user a moderator of the community?")

class ICatalogSearch(Interface):
    """Centralize policies about searching"""

class ITagQuery(Interface):
    """Centralize policies about listing tag information"""

    tagusers = Attribute("List the taguser information on a resource")

class ICatalogSearchCache(Interface):
    """ Utility which provides a cache for catalog searches """
    generation = Attribute('The current cache generation number')
    def clear():
        """ Clears the cache """
    def get(key, default=None):
        """ Return the value for ``key`` or ``None`` if no value """
    def __setitem__(key, val):
        """ Set the key to val """

class ICatalogQueryEvent(Interface):
    """Notification that a catalog was queried"""
    catalog = Attribute('The catalog that was queried')
    query = Attribute('Keyword parameters passed in the query')
    duration = Attribute('How long the query took, in seconds')
    result = Attribute('The result of the query: (result_count, [docid])')



class IIntranets(ICommunity):
    """ Mark the top of the intranet hierarchy e.g. /osi """
    taggedValue('name', 'Intranets')
    feature = Attribute('HTML for the feature portlet')

class IIntranet(IFolder):
    """ Mark an intranet community to attach views """
    taggedValue('name', 'Intranet')

class IAttachmentPolicy(Interface):
    """Policy controlling attachments"""

    def support():
        """Return true if the given object should support attachments"""

class IOrderedFolder(IFolder):
    """Orderable container
    """
    order = Attribute("Ordered sequence of IDs")

class IPeopleDirectory(IOrderedFolder):
    """Searchable directory of profiles.

    Contains IPeopleSection objects.
    """
    title = Attribute("Directory title")
    catalog = Attribute("Catalog of profiles")

class IPeopleCategories(Interface):
    """ Marker for the 'categories' container under a peopledir.
    """
    title = Attribute("Directory title")

class IPeopleCategory(Interface):
    """A vocabulary for profile category values.

    This object is a mapping. It maps an identifier for the category
    value (for example, 'payroll-department') to an object that
    implements IPeopleCategoryItem.
    """
    title = Attribute("The name of the category.  Example: 'Departments'")

    def __getitem__(value_id):
        """Return the specified IPeopleCategoryItem, or raise KeyError"""

    def get(value_id, default=None):
        """Return the specified IPeopleCategoryItem, or None"""

class IPeopleCategoryItem(Interface):
    """Metadata about a person category value."""
    title = Attribute(
        "Descriptive name.  Example: 'Human Resources'")
    description = Attribute(
        "An XHTML block that describes the category value")

class ISocial(Interface):
    """Interface to support social network linkage."""
    id = Attribute(
        "Social network user id.")

class IPeopleSection(IFolder):
    """Section of the people directory.

    Contains IPeopleReport objects.
    """
    title = Attribute("Section title")
    tab_title = Attribute("Title to put on the section tab")

class IPeopleSectionColumn(Interface):
    """A visual column within a section display
    """
    width = Attribute("Width of a section column")

class IPeopleReportGroup(Interface):
    """A group of reports displayed in a section
    """
    title = Attribute("Report group title")

class IPeopleReportFilter(Interface):
    """A filter for a report displayed in a section
    """
    values = Attribute("Category values for which the filter applies")

class IPeopleReportCategoryFilter(IPeopleReportFilter):
    """A category-based filter for a report displayed in a section
    """

class IPeopleReportGroupFilter(IPeopleReportFilter):
    """A group-based filter for a report displayed in a section
    """

class IPeopleReportIsStaffFilter(IPeopleReportFilter):
    """A staff filter for a report displayed in a section
    """
    include_staff = Attribute("Include staff in query?")

class IPeopleReportMailingList(Interface):
    """Marker object indicating that the parent report enables mailing list.
    """
    short_address = Attribute("Short / pretty e-mail prefix for the list.")

class IPeopleReport(Interface):
    """A report about people
    """
    title = Attribute("Report title")
    link_title = Attribute("Title to use for the link to the report")
    css_class = Attribute("CSS class of the link to the report")
    columns = Attribute("IDs of columns to display in the report.")

    def getQuery():
        """ Return a catalog query mapping corresponding to our criteria.
        """

class IPeopleRedirector(Interface):
    """Redirect to another url"""
    target_url = Attribute("Target URL")

class IPeopleDirectorySchemaChanged(Interface):
    """Notification that the schema of the people directory has changed"""
    peopledir = Attribute('The IPeopleDirectory object')

class ISiteEvents(Interface):
    """ Site-level 'tool' for tracking user event stream.

    Events are pushed as mappings.
    """
    def __iter__():
        """ Yield (generation, index, mapping) in most-recent first order.
        """

    def newer(latest_gen, latest_index, principals=None, created_by=None):
        """ Yield items newer than (`latest_gen`, `latest_index`).

        Implemented as a method on the layer to work around lack of generator
        expressions in Python 2.5.x.

        If 'principals' is passed, yield only items where mapping['allowed']
        contains one or more of the named principals.

        If 'created_by' is passed and is not None, yield only items where
        mapping['userid'] or mapping['content_creator'] is equal to its value.
        Communities are not ever yielded in this case.
        """

    def older(earliest_gen, earliest_index, principals=None, created_by=None):
        """ Yield items older than (`earliest_gen`, `earliest_index`).

        Implemented as a method on the layer to work around lack of generator
        expressions in Python 2.5.x.

        If 'principals' is passed, yield only items where mapping['allowed']
        contains one or more of the named principals.

        If 'created_by' is passed and is not None, yield only items where
        mapping['userid'] or mapping['content_creator'] is equal to its value.
        Communities are not ever yielded in this case.
        """

    def checked(principals, created_by):
        """ Yield (generation, index, mapping) in most-recent first order.

        Yield only items where mapping['allowed'] contains one or more of
        the named principals and (if 'created_by' is not None and item content
        is not a community) was created by the named userid.
        """

    def push(**kw):
        """ Append an mapping to the stack.
        """

class IBlog(IFolder):
    """A folder containing blog entries"""
    title = Attribute(u'Title of this Blog')
    description = Attribute(u'Blog description')
    taggedValue('name', 'Blog')

class IBlogEntry(IFolder):
    """A folder for a blog entry and its comments

    o The `comments` key returns a CommentsFolder
    o The `attachments` key returns an AttachmentsFolder

    """
    title = Attribute(u'Title of this Blog Post')
    summary = Attribute(u'Blog Entry summary for listings')
    text = Attribute(u'Blog Entry content')
    taggedValue('name', 'Blog Entry')
    taggedValue('search_option', True)

class IBlogCollection(IFolder):
    """ A collection of IBlog and IExternalFeed objects
    """
    title = Attribute(u'The name of the Blog collection')
    # junkafarian: Should this inherit from ICommunity?

## Bookmarking ##
class IBookmarkUtility(Interface):
    
    def save(user):
        """Register `user` against self.context"""
    
    def remove(user):
        """Unregister `user` against self.context"""
    
    def clear():
        """Clear all references"""


class IEventContainer(IFolder):
    """A folder that supports storage of calendar events"""

class ICalendar(IEventContainer):
    """A folder that holds a community's calendar events"""
    taggedValue('name', 'Calendar')

    title = Attribute(u'Title needed for backlinks')

class ICalendarEvent(ICommunityContent, IOthers):
    """A folder for a calendar event"""
    taggedValue('name', 'Event')
    taggedValue('search_option', True)

    title = Attribute(u'Event title')
    startDate = Attribute(u'DateTime object with value from form')
    endDate = Attribute(u'DateTime object with value from form')
    text = Attribute(u'Text description of event.')
    location = Attribute(u'Location of event.')
    attendees = Attribute(u'List of names of people attending event.')
    contact_name = Attribute(u'Name of person to contact about this event.')
    contact_email = Attribute(u'Email of person to contact about this event.')
    creator = Attribute(u'User id of user that created this event.')
    calendar_category = Attribute("Name of the associated calendar category")

class ICalendarLayer(Interface):
    taggedValue('default_name', '_default_layer_')
    title = Attribute(u'Layer title')
    color = Attribute(u'Layer color')
    paths = Attribute(u'Layer paths')

class ICalendarCategory(Interface):
    taggedValue('default_name', '_default_category_')
    title = Attribute(u'Calendar title')

class INewsItem(ICommunityContent, IFolder):
    """ A news item.
    """
    # These tagged values mean this content type should appear in the list of
    # types to search in the advanced search.
    taggedValue('name', 'News Item')
    taggedValue('search_option', True)

    title = Attribute(u'Title of news item.')
    text = Attribute(u'Body of news item.')
    publication_date = Attribute(u'Date item was (will be) published.')
    creator = Attribute(u'User id of user that created this news item.')
    caption = Attribute(u'Caption that appears under photo for this article.')

## Design Toolkit ##

class IDesignToolbox(IFolder):
    """ Marker interface for styling Design Toolbox pages
    """

class IPages(Interface):
    """Grouping for LiveSearch and other purposes"""
    taggedValue('name', 'Pages')

class IReferenceSection(IFolder, ICommunityContent, IPages):
    """A section of a reference manual in a community"""
    taggedValue('name', 'Reference Section')
    description = Attribute(u'Description')

class IReferenceManual(IReferenceSection):
    """A reference manual in a community"""
    taggedValue('name', 'Reference Manual')
    description = Attribute(u'Description')

class IReferenceManualHTML(Interface):
    """ Adapter interface for getting HTML for an item in a reference manual.
    """
    def __call__(api):
        """ Return an appropriate HTML fragment for our context.

        ``api`` may be used to generate URLs in rendered HTML.
        """

class IWiki(IFolder):
    """A folder containing wiki pages"""
    taggedValue('name', 'Wiki')

    title = Attribute(u'Title needed for backlinks')

class IWikiPage(IFolder, ICommunityContent, IPages):
    """A page using wiki markup
    """
    taggedValue('name', 'Wiki Page')
    taggedValue('search_option', True)
    text = Attribute(u'Text -- includes wiki markup.')

class IPage(IFolder):
    """A page that isn't in a wiki
    """
    #taggedValue('name', 'Page')
    title = Attribute(u'Title')
    text = Attribute(u'Text')
    description = Attribute(u'Short description of the page contents')
    
    display_menu = Attribute(u'Bool -- Whether to show structured navigation for this selection of pages')
    display_in_menu = Attribute(u'Bool -- Whether to show a link to this page in dynamically generated menus')


class ICommunityFolder(ICommunityContent, IFolder):
    """A folder in a community"""
    taggedValue('name', 'Folder')

class ICommunityRootFolder(IFolder):
    """The root folder under the Files tab in a community"""
    taggedValue('name', 'Files')

    title = Attribute(u'Title needed for backlinks')


class INewsFolder(ICommunityContent, IFolder):
    """ Marker for a newsitem folder that needs special layout """
    taggedValue('name', 'Folder')

class IEventsFolder(ICommunityContent, IFolder):
    """ Marker for an events folder that needs special layout"""
    taggedValue('name', 'Folder')

class IReferencesFolder(ICommunityContent, IFolder):
    """ Marker for a folder containing only reference manuals """
    taggedValue('name', 'Folder')


class ICommunityFile(ICommunityContent, IFiles):
    """A file in a community"""
    taggedValue('name', 'File')
    taggedValue('search_option', True)

    blobfile = Attribute(u'Optional file attachment')
    mimetype = Attribute(u'Content type')
    filename = Attribute(u'Uploaded filename')
    size = Attribute(u'Size in bytes')


class IImage(Interface):
    """ An image. """

    image_size = Attribute(u'Tuple of (width, height) in pixels.')

    def thumbnail(size):
        """
        Returns resized image bound by size, which is a tuple of
        (width, height).
        """

    def image():
        """
        Returns instance of PIL.Image.
        """

class IForumsFolder(IFolder):
    """ A folder that contains forums """
    taggedValue('name', 'Forums')

class IForum(IFolder, IPosts):
    """ A forum in a community """
    taggedValue('name', 'Forum')

class IForumTopic(ICommunityContent, IPosts):
    """ A topic in a forum """
    taggedValue('name', 'Forum Topic')

    text = Attribute(u"Form post content.")

class IOrdering(Interface):
    """ Persistent ordering of content in a folder """

    def sync(entries):
        """ Find mistakes between the ordering and context """

    def moveUp(name):
        """ Move an item up in the ordering """

    def moveDown(name):
        """ Move an item down in the ordering """

    def add(name):
        """ Add an item at the end of the ordering """

    def remove(name):
        """ Remove an item from the ordering """

    def items():
        """ Return the internal list of names in the ordering as list"""

    def previous_name(current_name):
        """ Given a name, return the previous name or None """

    def next_name(current_name):
        """ Given a name, return the next name or None """


class ILike(Interface):   
    """Like content""" 

class IEventInfo(Interface):
    """ SiteEvents event info"""
        
class IProfileDict(Interface):
    """ A dict-like profile.
    """
    def update_details(context, request):
        """ Updates the profile with additional information.
        """

class IPasswordRequestRequest(Interface):
    request_id = Attribute(u'Request ID')
    email = Attribute(u'e-mail')
    valid_from = Attribute(u'Valid from')
    valid_to = Attribute(u'Valid to')
    
    def get_valid_from_to():
        """ Return a two-element two of (valid_from, valid_to), indicating the
        timeframe for a user to change the password.
        """

class IUserAdded(Interface):
    """ Event interface for having a new user added to the system.
    """
    site = Attribute('The site object')
    id = Attribute('The unique identifier for the user')
    login = Attribute('The name under which the user logs in.')
    groups = Attribute('The initial set of groups to which the user belongs.')

class IUserRemoved(Interface):
    """ Event interface for having a user removed from the system.
    """
    site = Attribute('The site object')
    id = Attribute('The unique identifier for the user')
    login = Attribute('The name under which the user logs in.')
    groups = Attribute('The set of groups to which the user belongs.')

class IUserAddedGroup(Interface):
    """ Event interface for when a user has just added a new group.
    """
    site = Attribute('The site object')
    id = Attribute('The unique identifier for the user')
    login = Attribute('The name under which the user logs in.')
    groups = Attribute('The set of groups to which the user now belongs.')
    old_groups = Attribute('The set of groups to which the user '
                           'formerly belonged.')

class IUserRemovedGroup(Interface):
    """ Event interface for when a user has just removed a group.
    """
    site = Attribute('The site object')
    id = Attribute('The unique identifier for the user')
    login = Attribute('The name under which the user logs in.')
    groups = Attribute('The set of groups to which the user now belongs.')
    old_groups = Attribute('The set of groups to which the user '
                           'formerly belonged.')


# from openideo
class IExternalFeed(Interface):
    """ Should also have a photo.* attached if possible
    """
    title = Attribute(u'Title of the feed')
    uri = Attribute(u'Link to the RSS feed URL')
    
class IExternalReference(ICommunityContent, IFiles, IGalleryRenderable):
    """ A reference to external content
        (eg youtube/vimeo video or flickr stream)
    """
    taggedValue('name', 'External Reference')
    taggedValue('search_option', True)
    
    reference = Attribute(
        u'Reference to the content on the remote platform (eg content ID)')
    content_provider = Attribute(u'The platform this content is hosted on')
    
class IAdHocSchemaContainer(IFolder):
    pass

class IAdHocContentContainer(IFolder):
    pass

class IAdHocSchema(Interface):
    pass

class IAdHocContent(Interface):
    pass

## FAQ ##

class IFAQContainer(IFolder):
    """ Marker interface for a folder containing a series of IFAQ objects
    """

class IFAQ(IFolder):
    title = Attribute(u'Title of this FAQ section')
    text = Attribute(u'FAQ description')

class IFAQQuestion(Interface):
    title = Attribute(u'Question Title')
    question = Attribute(u'Frequently Asked Question')
    answer = Attribute(u'Answer')

class IWorkflow(Interface):
    status = Attribute(u'The current workflow status of the object')

class IObjectActionEvent(IObjectEvent):
    """Base class for events that get fired on content actions,
       e.g. flagging content etc."""
    
class IContentAddedEvent(IObjectActionEvent):
    """Content was added"""
    
class IContentApplaudedEvent(IObjectActionEvent):
    """Content was applauded"""

class IContentCommentedEvent(IObjectActionEvent):
    """Content was commented"""

class IContentFlaggedEvent(IObjectActionEvent):
    """Content was flagged"""

class IContentRatedEvent(IObjectActionEvent):
    """Content was rated"""

class IContentPublishedEvent(IObjectActionEvent):
    """Content was published"""

class IContentUnpublishedEvent(IObjectActionEvent):
    """Content was unpublished"""

class IContentBaseonEvent(IObjectActionEvent):
    """Content was based on something"""
    
class IContentFirstEntryEvent(IObjectActionEvent):
    """Content type was added for the first time""" 

class IAssignmentsContainer(IFolder):
    pass

class IAssignment(IFolder):
    pass

class ILabelsContainer(IFolder):
    pass

class ILabels(IFolder):
    pass

class IHasFeed(Interface):
    pass

class IStaticPage(Interface):
    taggedValue('name', 'Static Pages')


class IGroupSearch(Interface):
    def __call__():
        """ Return num, docids, resolver for a full search """

    def get_batch():
        """ Return a single batch of results (based on request information) """