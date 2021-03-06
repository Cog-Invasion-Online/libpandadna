#ifndef _H_DNA_LANDMARK_
#define _H_DNA_LANDMARK_

#include "DNANode.h"

class EXPCL_DNA DNALandmarkBuilding : public DNANode
{
    PUBLISHED:
        DNALandmarkBuilding(const std::string& name);
        ~DNALandmarkBuilding();
        
        WRITE_PDNA
        {
            DNANode::write_pdna(dg, false);
            
            dg.add_string(m_code);
            pack_color(dg, m_wall_color);
            
            if (recursive)
                pack_children_pdna(dg);
        }
        
        WRITE_DNA
        {
            DNANode::write_dna(out, false, indent);
            indent += 1;
            
            if (m_wall_color != LVecBase4f(1, 1, 1, 1))
                INDENTED_OUT << "color [ " << m_wall_color.get_x() << " "
                             << m_wall_color.get_y() << " " << m_wall_color.get_z()
                             << " " << m_wall_color.get_w() << " ]" << std::endl;
                             
            if (m_code.size())
                INDENTED_OUT << "code [ \"" << m_code << "\" ]" << std::endl;
            
            if (recursive)
                pack_children_dna(out, indent - 1);
        }
        
        COMP_CODE(COMPCODE_LANDMARK_BUILDING);
        COMP_NAME(landmark_building);

    public:
        virtual void make_from_dgi(DatagramIterator& dgi, DNAStorage* store);
        virtual void traverse(NodePath& np, DNAStorage* store);
        
    protected:
        void setup_suit_building_origin(NodePath& a, NodePath& b);
        
    PROPERTY_COLOR(wall_color);
    PROPERTY_STRING(code);
    
    TYPE_HANDLE(DNALandmarkBuilding, DNANode);
};

#endif
