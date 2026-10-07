"""Review accepted single-ring room polygons in an explicit served-level frame.

Never modifies geometry or model membership. Notch editing remains owner-reviewed.
"""
from shapely.geometry import Point, Polygon


def _polygons(footprints):
    result={}
    for f in footprints:
        sid=f['space_id']
        if sid in result: raise ValueError('Use one footprint per Space in this frame review.')
        if not f.get('level') or not f.get('frame_id'):
            raise ValueError('Known served level and registered coordinate frame are required.')
        shape=Polygon(f['vertices'])
        if shape.is_empty or not shape.is_valid or shape.area<=0 or shape.interiors:
            raise ValueError('Room must be a valid positive-area single ring; no holes or zero-width slits.')
        result[sid]=(f,shape)
    return result


def derive_nested_in(footprints):
    """Smallest full-containing host on the same level and coordinate frame."""
    shapes=_polygons(footprints); result={}
    for sid,(f,shape) in shapes.items():
        candidates=[(host.area,hid) for hid,(h,host) in shapes.items()
                    if hid!=sid and h['level']==f['level'] and h['frame_id']==f['frame_id']
                    and host.area>shape.area and host.covers(shape)]
        candidates.sort()
        if len(candidates)>1 and candidates[0][0]==candidates[1][0]:
            raise ValueError('Equal-area containing hosts require explicit review.')
        result[sid]=candidates[0][1] if candidates else None
    return result


def smallest_containing_space(point, footprints, level, frame_id):
    """Served-level membership proposal; unresolved ties/outside points fail closed."""
    shapes=_polygons(footprints)
    candidates=sorted((shape.area,sid) for sid,(f,shape) in shapes.items()
                      if f['level']==level and f['frame_id']==frame_id
                      and f.get('eligible_for_lights',True) and shape.covers(Point(point)))
    if not candidates: raise ValueError('No containing served Space; retain unresolved/excluded inventory.')
    if len(candidates)>1 and candidates[0][0]==candidates[1][0]:
        raise ValueError('Boundary/equal-area tie requires review.')
    return candidates[0][1]


def room_draw_order(footprints):
    shapes=_polygons(footprints)
    return sorted(footprints,key=lambda f:-shapes[f['space_id']][1].area)
